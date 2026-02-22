import os
import time
from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from schema import APIInput
from search_agent import main
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time(), "version": "2.0.0"}

@app.post('/research_agent/')
async def research_agent_endpoint(state: APIInput, api_key: str = Query(None)):    
    expected_key = os.getenv("RESEARCH_API_KEY")
    # If a key is set in .env, require it
    if expected_key and api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
        
    try:
        events = await main(query=state.query, mode=state.mode)
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
