from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.vector_store import search_similar_docs
from agents.responder_agent import generate_response
from fastapi.responses import JSONResponse

app = FastAPI()

class QueryRequest(BaseModel):
    user_id: str
    query: str

@app.post("/query")
async def query_bot(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        # Recuperar documentos relevantes usando el vector store
        docs = search_similar_docs(request.query, k=3)
        
        # Generar respuesta usando el agente responder
        answer = generate_response(request.query, docs)
        
        return {
            "user_id": request.user_id, 
            "answer": answer,
            "status": "success"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
