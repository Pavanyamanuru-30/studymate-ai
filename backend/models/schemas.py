from pydantic import BaseModel, Field
from typing import List

class QueryRequest(BaseModel):
    query: str = Field(..., description="The user's question.", min_length=3)
    document_id: str = Field(..., description="The ID of the document to query against.")

class QueryResponse(BaseModel):
    answer: str = Field(..., description="The AI-generated answer.")
    sources: List[str] = Field(default_factory=list, description="The retrieved chunks used for context.")
    confidence: str = Field(default="High", description="An observability indicator of groundedness.")

class UploadResponse(BaseModel):
    document_id: str = Field(..., description="The unique ID of the uploaded document.")
    filename: str = Field(..., description="The name of the uploaded file.")
    chunks_indexed: int = Field(..., description="Number of text chunks indexed.")
