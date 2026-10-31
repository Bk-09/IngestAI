from app.validator import validate

TEXT = "Acme Corp reported revenue of $4.2 billion. Headcount grew 18%."

def good(**overrides):
    d = {"company_name": "Acme Corp", "reported_revenue": 4.2e9,
         "revenue_currency": "USD", "headcount_growth_percentage": 18,
         "key_product_launch": None}
    d.update(overrides)
    return d

def test_valid_passes():
    item, errors = validate(good(), TEXT)
    assert item is not None and errors == []

def test_text_in_revenue_field_fails():
    item, errors = validate(good(reported_revenue="up by 20%"), TEXT)
    assert item is None and any("reported_revenue" in e for e in errors)

def test_invalid_currency():
    _, errors = validate(good(revenue_currency="DOLLARS"), TEXT)
    assert any("ISO" in e for e in errors)

def test_negative_revenue():
    _, errors = validate(good(reported_revenue=-5), TEXT)
    assert errors

def test_revenue_without_currency():
    _, errors = validate(good(revenue_currency=None), TEXT)
    assert any("required" in e for e in errors)

def test_hallucinated_company():
    _, errors = validate(good(company_name="Globex"), TEXT)
    assert any("hallucination" in e for e in errors)

def test_implausible_growth():
    _, errors = validate(good(headcount_growth_percentage=5000), TEXT)
    assert errors