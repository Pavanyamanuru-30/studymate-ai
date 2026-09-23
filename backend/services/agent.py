import os
from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END
from google import genai
from backend.services.embedding import EmbeddingService

class RAGState(TypedDict):
    doc_id: str
    original_query: str
    refined_query: str
    context: List[str]
    answer: str
    confidence: str

embedding_service = EmbeddingService()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def refine_query_node(state: RAGState) -> RAGState:
    """Agent step: Refine the query for better retrieval if it's too vague."""
    query = state["original_query"]
    # For a full production system, we could ask the LLM to rewrite the query here.
    # To keep it fast, we'll just trim and optimize simple queries.
    refined = query.strip().lower()
    if len(refined.split()) < 3:
        refined = f"explain {refined} in detail based on the document"
    state["refined_query"] = refined
    return state

def retrieve_node(state: RAGState) -> RAGState:
    """Agent step: Vector search against FAISS."""
    context_chunks = embedding_service.retrieve_context(state["doc_id"], state["refined_query"])
    state["context"] = context_chunks
    return state

def generate_node(state: RAGState) -> RAGState:
    """Agent step: Generate grounded answer."""
    context_str = "\n\n---\n\n".join(state["context"])
    prompt = f"""You are a production RAG assistant. 
Answer the following question using strictly the provided context. If the answer is not in the context, explicitly say so to avoid hallucination.

CONTEXT:
{context_str}

QUESTION:
{state["original_query"]}
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash", 
            contents=prompt,
        )
        state["answer"] = response.text
        # Naive confidence check:
        if "I cannot find the answer" in response.text or "not in the context" in response.text:
            state["confidence"] = "Low (Not in document)"
        else:
            state["confidence"] = "High (Grounded)"
    except Exception as e:
        state["answer"] = f"Generation failed: {str(e)}"
        state["confidence"] = "Error"
        
    return state

# Compile LangGraph
workflow = StateGraph(RAGState)
workflow.add_node("refine", refine_query_node)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate", generate_node)

workflow.set_entry_point("refine")
workflow.add_edge("refine", "retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

rag_agent = workflow.compile()

def run_agent(doc_id: str, query: str):
    initial_state = {
        "doc_id": doc_id,
        "original_query": query,
        "refined_query": "",
        "context": [],
        "answer": "",
        "confidence": ""
    }
    final_state = rag_agent.invoke(initial_state)
    return final_state
