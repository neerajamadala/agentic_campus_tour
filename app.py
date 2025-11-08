# app.py
from fastapi import FastAPI
from fastapi.responses import FileResponse
from agent import agent

app = FastAPI(title="Agentic AI Campus Guide")

# Serve UI
@app.get("/")
def serve_ui():
    return FileResponse("index.html")

# Ask endpoint
@app.get("/ask")
def ask_agent(query: str):
    """
    Example usage:
    /ask?query=Where%20is%20the%20library?
    """
    try:
        response = agent.run(query)
        if not isinstance(response, str):
            response = str(response)
        return {"query": query, "response": response}
    except Exception as e:
        return {"query": query, "response": f"Campus Guide: Sorry, I couldn't process that query. ({str(e)})"}
