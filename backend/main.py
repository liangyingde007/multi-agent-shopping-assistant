from fastapi import FastAPI
from workflow.graph import run_workflow

app = FastAPI(title="Multi-Agent Shopping Assistant")

@app.get("/")
def health():
    return {"status":"running"}

@app.post("/chat")
def chat(query:str):
    return {"answer": run_workflow(query)}
