
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from scorer import score_payload, resolve_pattern

app = FastAPI(title="BCAT Alignment Service (Curated 10 Metrics + 24 Patterns)")

class ScoreRequest(BaseModel):
    spiky: Dict[str, Any]
    pattern_id: Optional[int] = Field(default=None)
    pattern_name: Optional[str] = Field(default=None)
    bcat_pattern: Optional[List[str]] = Field(default=None)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/score")
def score(req: ScoreRequest):
    order = resolve_pattern(req.pattern_id, req.pattern_name, req.bcat_pattern)
    try:
        return score_payload(req.spiky, order)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
