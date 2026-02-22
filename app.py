from fastapi import FastAPI, Query, HTTPException
from schema import APIInput
from search_agent import main

app = FastAPI()

@app.post('/research_agent/')
async def research_agent_endpoint(state: APIInput, api_key: str = Query(...)):    
    try:
        events = await main(query=state.query,mode=state.mode)
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
