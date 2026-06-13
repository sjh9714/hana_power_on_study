from docling.document_converter import DocumentConverter

converter = DocumentConverter()

doc = converter.convert("data/sample.pdf")

print(doc.document.export_to_markdown())
