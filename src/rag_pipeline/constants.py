import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

KNOWLEDGE_BASE_FILE_PATH = str(Path(__file__).parent.parent /
                "knowledge-base" / "case-studies.txt")

VECTOR_STORE_COLLECTION_NAME = 'case-studies'

QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')

EMBEDDING_MODEL = 'text-embedding-3-large'
