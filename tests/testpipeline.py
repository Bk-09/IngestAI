from app import pipeline

TEXT = "Acme Corp reported revenue of $4.2 billion."

def test_loop_self_corrects(monkeypatch):
    outputs = iter([
        {"company_name": "Acme Corp", "reported_revenue": 4.2e9, "revenue_currency": "DOLLARS"},
        {"company_name": "Acme Corp", "reported_revenue": 4.2e9, "revenue_currency": "USD"},
    ])
    monkeypatch.setattr(pipeline, "extract", lambda *a, **k: next(outputs))
    monkeypatch.setattr(pipeline, "upsert", lambda data, attempts: "created")
    result = pipeline.run_pipeline(TEXT)
    assert result["status"] == "success"
    assert len(result["trace"]) == 2   # failed once, then fixed

def test_loop_gives_up(monkeypatch):
    bad = {"company_name": "Acme Corp", "reported_revenue": 4.2e9, "revenue_currency": "XXX"}
    monkeypatch.setattr(pipeline, "extract", lambda *a, **k: bad)
    result = pipeline.run_pipeline(TEXT)
    assert result["status"] == "failed"
    assert len(result["trace"]) == 3   # MAX_ATTEMPTS