from .extractor import extract
from .validator import validate
from .db import upsert

MAX_ATTEMPTS = 3

def run_pipeline(text: str) -> dict:
    raw, errors, trace = None, None, []
    for attempt in range(1, MAX_ATTEMPTS + 1):
        raw = extract(text, previous=raw, errors=errors)
        item, errors = validate(raw, text)
        trace.append({"attempt": attempt, "output": raw, "errors": errors})
        if item:
            action = upsert(item.model_dump(), attempt)
            return {"status": "success", "action": action, "data": item.model_dump(), "trace": trace}
    return {"status": "failed", "reason": "validation failed after max attempts", "trace": trace}