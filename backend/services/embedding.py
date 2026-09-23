import os
import uuid
from typing import List, Dict
import numpy as np
import faiss
import PyPDF2
import io
from google import genai
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

EMBEDDING_MODEL = "gemini-embedding-2"

# In-memory storage for prototype. In production, use Redis or Postgres.
DOCUMENT_STORE: Dict[str, Dict] = {}

class EmbeddingService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)

    def extract_text(self, file_bytes: bytes, filename: str) -> str:
        """Parse multi-format documents (currently supports PDF, TXT)"""
        text = ""
        if filename.endswith('.pdf'):
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        else:
            text = file_bytes.decode('utf-8', errors='ignore')
        return text

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    def embed_chunks(self, chunks: List[str]) -> np.ndarray:
        embeddings = []
        for chunk in chunks:
            if not chunk.strip():
                continue
            try:
                response = self.client.models.embed_content(
                    model=EMBEDDING_MODEL,
                    contents=chunk,
                )
                embeddings.append(response.embeddings[0].values)
            except Exception as e:
                logger.error(f"Error embedding chunk: {e}")
        return np.array(embeddings, dtype=np.float32)

    def process_document(self, file_bytes: bytes, filename: str) -> str:
        """End-to-end ingestion pipeline"""
        raw_text = self.extract_text(file_bytes, filename)
        if not raw_text.strip():
            raise ValueError("No extractable text found.")

        chunks = self.chunk_text(raw_text)
        embeddings = self.embed_chunks(chunks)

        if len(embeddings) == 0:
            raise ValueError("Failed to generate embeddings.")

        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)

        doc_id = str(uuid.uuid4())
        DOCUMENT_STORE[doc_id] = {
            "filename": filename,
            "chunks": chunks,
            "index": index
        }
        return doc_id

    def retrieve_context(self, doc_id: str, query: str, top_k: int = 3) -> List[str]:
        if doc_id not in DOCUMENT_STORE:
            raise ValueError("Document not found.")
        
        doc_data = DOCUMENT_STORE[doc_id]
        query_embedding = self.embed_chunks([query])
        
        if len(query_embedding) == 0:
            return []

        distances, indices = doc_data["index"].search(query_embedding, top_k)
        
        retrieved = []
        for idx in indices[0]:
            if idx < len(doc_data["chunks"]) and idx != -1:
                retrieved.append(doc_data["chunks"][idx])
        return retrieved

embedding_service = EmbeddingService()

