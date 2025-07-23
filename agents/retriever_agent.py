from core.vector_store import search_similar_docs

def retrieve_documents(query: str):
    return search_similar_docs(query)
