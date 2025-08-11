import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"
CHROMA_DB_DIR = "chroma_db"
SUMMARY_FILE = "book_summaries.json"