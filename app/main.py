from fastapi import FastAPI
from pydantic import BaseModel
from .db import init_db, get_conn
from .pipeline import run_pipeline

app = FastAPI(title="Competitor Intel Pipeline")
init_db()

class IngestRequest(BaseModel):
    text: str

@app.post("/ingest")
def ingest(req: IngestRequest):
    return run_pipeline(req.text)

@app.get("/insights")
def insights():
    with get_conn() as c:
        return [dict(r) for r in c.execute("SELECT * FROM competitor_insights ORDER BY updated_at DESC")]