import os
import time
import json
import hashlib
import logging
from datetime import datetime

import feedparser
import requests
from bs4 import BeautifulSoup
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import chromadb
from chromadb.config import Settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Config
WORKDIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(WORKDIR, 'index.json')
CHROMA_DIR = os.path.join(WORKDIR, 'chroma_db')
FEEDS_FILE = os.path.join(WORKDIR, 'feeds.txt')

# Default RSS feeds (can be overridden by editing feeds.txt)
DEFAULT_FEEDS = [
    'http://feeds.reuters.com/reuters/businessNews',
    'https://news.google.com/rss/search?q=financial+news&hl=en-US&gl=US&ceid=US:en'
]

EMBED_MODEL_NAME = os.environ.get('EMBED_MODEL', 'all-MiniLM-L6-v2')
CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', 1000))
CHUNK_OVERLAP = int(os.environ.get('CHUNK_OVERLAP', 200))


def load_feeds():
    if os.path.exists(FEEDS_FILE):
        with open(FEEDS_FILE, 'r', encoding='utf-8') as f:
            feeds = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        if feeds:
            return feeds
    return DEFAULT_FEEDS


def load_index():
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_index(index):
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def fetch_article_content(url: str, timeout=15) -> str:
    try:
        resp = requests.get(url, timeout=timeout, headers={'User-Agent': 'news-collector/1.0'})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Collect text from paragraphs
        paragraphs = soup.find_all('p')
        text = '\n'.join(p.get_text(strip=True) for p in paragraphs)
        if text.strip():
            return text
        # fallback to body text
        body = soup.get_text(separator='\n')
        return body
    except Exception as e:
        logging.debug('Failed to fetch article %s: %s', url, e)
        return ''


def ensure_chroma_client():
    os.makedirs(CHROMA_DIR, exist_ok=True)
    client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=CHROMA_DIR))
    collection = client.get_or_create_collection(name="financial_news")
    return client, collection


def process_feeds(feeds, index, model, collection, client):
    updated = False
    for feed_url in feeds:
        logging.info('Parsing feed: %s', feed_url)
        try:
            parsed = feedparser.parse(feed_url)
        except Exception as e:
            logging.warning('Failed to parse feed %s: %s', feed_url, e)
            continue

        for entry in parsed.entries:
            url = entry.get('link') or entry.get('id')
            if not url:
                continue
            title = entry.get('title', '')
            summary = entry.get('summary', '')
            published = entry.get('published', '')

            content = fetch_article_content(url)
            if not content:
                content = summary or title

            content_hash = sha256(content)
            doc_id = sha256(url)

            prev = index.get(url)
            if prev and prev.get('hash') == content_hash:
                logging.debug('No change for %s', url)
                continue

            # New or changed article
            logging.info('New/updated article: %s', title or url)

            # split into chunks and embed via LangChain wrapper
            splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
            chunks = splitter.split_text(content)
            if not chunks:
                chunks = [content]

            try:
                embeddings = model.embed_documents(chunks)
            except Exception as e:
                logging.error('Embedding failed for %s: %s', url, e)
                continue

            ids = []
            docs = []
            metadatas = []
            for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
                chunk_id = f"{doc_id}_{i}"
                ids.append(chunk_id)
                docs.append(chunk)
                metadatas.append({
                    'title': title,
                    'url': url,
                    'published': published,
                    'chunk_index': i,
                    'fetched_at': datetime.utcnow().isoformat() + 'Z'
                })

            # If previous versions exist, delete their chunks
            if prev and prev.get('ids'):
                try:
                    collection.delete(ids=prev['ids'])
                except Exception:
                    logging.debug('Failed to delete previous ids for %s', url)

            try:
                collection.upsert(
                    ids=ids,
                    embeddings=embeddings,
                    metadatas=metadatas,
                    documents=docs,
                )
                client.persist()
            except Exception as e:
                logging.error('Failed to upsert into ChromaDB: %s', e)
                continue

            index[url] = {'hash': content_hash, 'ids': ids, 'title': title}
            updated = True

    if updated:
        save_index(index)


def main():
    feeds = load_feeds()
    index = load_index()

    logging.info('Loading LangChain embedding model: %s', EMBED_MODEL_NAME)
    model = SentenceTransformerEmbeddings(model_name=EMBED_MODEL_NAME)

    client, collection = ensure_chroma_client()

    logging.info('Starting collector loop (interval=600s)')
    try:
        while True:
            process_feeds(feeds, index, model, collection, client)
            logging.info('Sleeping 600s until next run')
            time.sleep(600)
    except KeyboardInterrupt:
        logging.info('Interrupted, exiting')


if __name__ == '__main__':
    main()
