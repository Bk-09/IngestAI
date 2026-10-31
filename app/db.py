import sqlite3

def get_conn():
    conn = sqlite3.connect("intel.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS competitor_insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_key TEXT NOT NULL UNIQUE,
            company_name TEXT NOT NULL,
            reported_revenue REAL,
            revenue_currency TEXT,
            headcount_growth_percentage REAL,
            key_product_launch TEXT,
            attempts INTEGER,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")

def company_key(name: str) -> str:
    return "".join(ch for ch in name.lower() if ch.isalnum())

def upsert(data: dict, attempts: int) -> str:
    key = company_key(data["company_name"])
    with get_conn() as c:
        existed = c.execute(
            "SELECT 1 FROM competitor_insights WHERE company_key=?", (key,)
        ).fetchone()
        c.execute("""
        INSERT INTO competitor_insights
          (company_key, company_name, reported_revenue, revenue_currency,
           headcount_growth_percentage, key_product_launch, attempts)
        VALUES (?,?,?,?,?,?,?)
        ON CONFLICT(company_key) DO UPDATE SET
          reported_revenue=excluded.reported_revenue,
          revenue_currency=excluded.revenue_currency,
          headcount_growth_percentage=excluded.headcount_growth_percentage,
          key_product_launch=excluded.key_product_launch,
          attempts=excluded.attempts,
          updated_at=CURRENT_TIMESTAMP
        """, (key, data["company_name"], data.get("reported_revenue"),
              data.get("revenue_currency"), data.get("headcount_growth_percentage"),
              data.get("key_product_launch"), attempts))
    return "updated" if existed else "created"