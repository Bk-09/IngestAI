from pydantic import BaseModel

class Extraction(BaseModel):
    company_name: str
    reported_revenue: float | None = None
    revenue_currency: str | None = None
    headcount_growth_percentage: float | None = None
    key_product_launch: str | None = None