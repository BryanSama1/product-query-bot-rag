from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.rag_pipeline import run_rag_pipeline

app = FastAPI()

class QueryRequest(BaseModel):
    user_id: str
    query: str

@app.post("/query")
async def query(req: QueryRequest):
    if not req.query or not req.user_id:
        raise HTTPException(status_code=400, detail="Invalid input")
    
    response = run_rag_pipeline(req.user_id, req.query)
    return {"response": response}
