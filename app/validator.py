from pydantic import ValidationError
from .schemas import Extraction

ISO_CURRENCIES = {"USD","EUR","GBP","INR","JPY","CNY","AUD","CAD","CHF","SGD","AED","SEK","BRL"}

def validate(raw: dict, source_text: str):
    errors = []
    try:
        item = Extraction(**raw)
    except ValidationError as e:
        for err in e.errors():
            errors.append(f"Field '{err['loc'][0]}': {err['msg']}")
        return None, errors

    if item.company_name.strip().lower() not in source_text.lower():
        errors.append("company_name does not appear in the article text (possible hallucination).")
    if item.reported_revenue is not None:
        if item.reported_revenue <= 0:
            errors.append("reported_revenue must be a positive number.")
        if not item.revenue_currency:
            errors.append("revenue_currency is required when reported_revenue is set.")
    if item.revenue_currency and item.revenue_currency.upper() not in ISO_CURRENCIES:
        errors.append(f"revenue_currency '{item.revenue_currency}' is not a valid ISO 4217 code.")
    if item.headcount_growth_percentage is not None and not -100 <= item.headcount_growth_percentage <= 1000:
        errors.append("headcount_growth_percentage is outside a plausible range (-100 to 1000).")

    return (item if not errors else None), errors