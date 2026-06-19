# 금융뉴스 수집기 (ChromaDB 저장)

간단한 RSS 기반 크롤러로 금융 관련 뉴스를 주기적으로 수집하여 ChromaDB에 임베딩과 함께 저장합니다.

설치

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

설정

- 피드 목록을 `feeds.txt`에 한 줄씩 추가합니다.
- 임베딩 모델 변경은 환경변수 `EMBED_MODEL`로 설정합니다 (기본: `all-MiniLM-L6-v2`).
- LangChain의 `SentenceTransformerEmbeddings`와 `CharacterTextSplitter`를 사용하여 텍스트를 분할하고 임베딩합니다.

실행

```bash
python news_collector.py
```

동작

- 10분(600초)마다 `feeds.txt`의 RSS를 파싱합니다.
- 기사의 URL을 기준으로 내용을 가져와 해시를 계산하고, 새 기사거나 변경된 기사일 때만 임베딩을 생성하여 ChromaDB에 upsert합니다.
- 로컬에 `index.json`(url→hash 매핑)과 `chroma_db`(Chroma 저장소)가 생성됩니다.

참고

- 프로덕션에서는 시스템 서비스(예: systemd, Windows 서비스)나 컨테이너로 운영하세요.
- 더 정교한 본문 추출 및 중복 처리(중복 유사도 검사 등)는 필요에 따라 확장하세요.
