from pathlib import Path
from typing import Literal
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator
from workflow.graph import run_workflow

app = FastAPI(title="Shopping Assistant Demo", version="0.2.0")
WEB_DIR = Path(__file__).resolve().parents[1] / "web"
Priority = Literal["camera", "performance", "battery", "portable", "value", "office", "gaming", "audio", "noise"]

class ChatRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    budget: int | None = Field(default=None, ge=1, le=100000)
    category: Literal["phone", "laptop", "headphones"] | None = None
    priorities: list[Priority] = Field(default_factory=list, max_length=9)

    @field_validator("query")
    @classmethod
    def check_query(cls, value):
        if not value.strip():
            raise ValueError("query must contain a shopping need")
        return value.strip()

@app.get("/")
def home():
    return FileResponse(WEB_DIR / "index.html")

@app.get("/healthz")
def health():
    return {"status": "ok", "version": "0.2.0", "data_mode": "sample"}

@app.post("/api/chat")
def chat(body: ChatRequest):
    return {"answer": run_workflow(body.query, body.budget, body.category, body.priorities)}

@app.post("/chat", include_in_schema=False)
def legacy_chat(query: str = Query(min_length=1, max_length=500)):
    return {"answer": run_workflow(query)}

app.mount("/assets", StaticFiles(directory=WEB_DIR), name="assets")
