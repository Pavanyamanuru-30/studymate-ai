from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.models.schemas import QueryRequest, QueryResponse, UploadResponse
from backend.services.embedding import embedding_service, DOCUMENT_STORE
from backend.services.agent import run_agent

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Ingest, chunk, and embed a document."""
    try:
        contents = await file.read()
        doc_id = embedding_service.process_document(contents, file.filename)
        chunks_count = len(DOCUMENT_STORE[doc_id]["chunks"])
        
        return UploadResponse(
            document_id=doc_id,
            filename=file.filename,
            chunks_indexed=chunks_count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=QueryResponse)
async def query_document(request: QueryRequest):
    """Agentic RAG pipeline query execution."""
    if request.document_id not in DOCUMENT_STORE:
        raise HTTPException(status_code=404, detail="Document not found. Please upload it first.")
        
    try:
        result = run_agent(request.document_id, request.query)
        return QueryResponse(
            answer=result["answer"],
            sources=result["context"],
            confidence=result["confidence"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
