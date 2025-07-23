from agents.retriever_agent import retrieve_documents
from agents.responder_agent import generate_response

def run_rag_pipeline(user_id: str, query: str) -> str:
    context_docs = retrieve_documents(query)
    response = generate_response(query, context_docs)
    return response
