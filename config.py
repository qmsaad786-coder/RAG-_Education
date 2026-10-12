import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data")
CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_db")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K = 4