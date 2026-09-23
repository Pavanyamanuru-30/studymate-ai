import io
from typing import List, Tuple
import PyPDF2
import numpy as np
import faiss
from google import genai
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

EMBEDDING_MODEL = "gemini-embedding-2"

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from an uploaded PDF file."""
    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into overlapping chunks for better retrieval context."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def get_embeddings(texts: List[str]) -> np.ndarray:
    """
    Generate embeddings for a list of strings using Gemini API.
    Returns a numpy array of embeddings.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    # Process in batches if necessary, but for now we'll do a simple list comprehension
    # The new google-genai SDK supports embedding multiple contents
    embeddings = []
    for text in texts:
        if not text.strip():
            continue
        try:
            response = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=text,
            )
            embeddings.append(response.embeddings[0].values)
        except Exception as e:
            logger.error(f"Error embedding chunk: {e}")
            
    return np.array(embeddings, dtype=np.float32)

def create_faiss_index(embeddings: np.ndarray) -> faiss.IndexFlatL2:
    """Create a FAISS vector index from embeddings."""
    if len(embeddings) == 0:
        raise ValueError("No embeddings generated. Please check the PDF content or API connectivity.")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def search_index(query: str, index: faiss.IndexFlatL2, chunks: List[str], top_k: int = 3) -> List[str]:
    """Embed the query, search the FAISS index, and return top_k matching chunks."""
    query_embedding = get_embeddings([query])
    if len(query_embedding) == 0:
        return []
    
    distances, indices = index.search(query_embedding, top_k)
    
    retrieved_chunks = []
    for idx in indices[0]:
        if idx < len(chunks) and idx != -1:
            retrieved_chunks.append(chunks[idx])
            
    return retrieved_chunks
