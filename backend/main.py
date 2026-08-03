from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import uvicorn
import uuid
import os
from typing import List, Optional

import config
from graph import build_graph
from state import GraphState

app = FastAPI(title="Enterprise HR AI Agent API")

# Setup CORS for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev purposes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    user_query: str
    employee_id: str

@app.post("/api/query")
async def run_query(req: QueryRequest):
    try:
        graph_app = build_graph()
        initial_state = {
            "trace_id": str(uuid.uuid4()),
            "query_id": f"Q-{uuid.uuid4().hex[:6].upper()}",
            "employee_id": req.employee_id,
            "user_query": req.user_query
        }
        result = graph_app.invoke(initial_state)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs")
async def get_logs():
    if not config.RESULTS_CSV.exists():
        return {"logs": []}
    try:
        df = pd.read_csv(config.RESULTS_CSV)
        # fillna to avoid JSON NaN issues
        df = df.fillna("")
        return {"logs": df.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/metrics")
async def get_metrics():
    if not config.RESULTS_CSV.exists():
        return {
            "total_queries": 0,
            "successful_requests": 0,
            "security_blocks": 0,
            "authorization_blocks": 0,
            "average_confidence": 0.0,
            "intents": {}
        }
    try:
        df = pd.read_csv(config.RESULTS_CSV)
        
        total = len(df)
        security_blocks = int(df['security_flag'].sum()) if 'security_flag' in df.columns else 0
        
        auth_blocks = 0
        if 'auth_approved' in df.columns:
            # count where auth_approved is False/0
            auth_blocks = len(df[df['auth_approved'] == False])
            
        success = total - security_blocks - auth_blocks
        
        avg_conf = 0.0
        if 'confidence_score' in df.columns:
            avg_conf = float(df['confidence_score'].mean())
            
        intents = {}
        if 'intent' in df.columns:
            intents = df['intent'].value_counts().to_dict()

        return {
            "total_queries": total,
            "successful_requests": success,
            "security_blocks": security_blocks,
            "authorization_blocks": auth_blocks,
            "average_confidence": round(avg_conf, 2),
            "intents": intents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/settings")
async def get_settings():
    return {
        "llm_provider": config.LLM_PROVIDER,
        "pinecone_status": "Enabled" if config.PINECONE_API_KEY else "Offline",
        "langsmith_status": "Enabled" if config.LANGCHAIN_TRACING_V2 else "Offline",
        "backend_health": "Healthy",
        "environment": "Development"
    }

@app.post("/api/batch")
async def upload_batch(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")
        
    try:
        content = await file.read()
        temp_path = config.DATA_DIR / "temp_upload.csv"
        with open(temp_path, "wb") as f:
            f.write(content)
            
        # Process inline to return results immediately for demo
        df_inputs = pd.read_csv(temp_path)
        graph_app = build_graph()
        
        results = []
        for index, row in df_inputs.iterrows():
            employee_id = str(row.get("employee_id", "")).strip()
            user_query = str(row.get("user_query", "")).strip()
            
            initial_state = {
                "trace_id": str(uuid.uuid4()),
                "query_id": f"BQ-{index+1}-{uuid.uuid4().hex[:4].upper()}",
                "employee_id": employee_id,
                "user_query": user_query
            }
            try:
                res = graph_app.invoke(initial_state)
                results.append(res)
            except Exception as e:
                initial_state["draft_response"] = f"Error: {str(e)}"
                results.append(initial_state)
                
        # Clean up
        if temp_path.exists():
            temp_path.unlink()
            
        return {"status": "success", "processed": len(results), "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
