import os, json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("LLM_API_KEY"), base_url=os.getenv("LLM_BASE_URL"))
MODEL = os.getenv("LLM_MODEL")

SYSTEM = """Extract competitor intelligence from the article. Return ONLY JSON with keys:
company_name (string), reported_revenue (number in full units, e.g. 4200000000 for $4.2B, or null),
revenue_currency (ISO 4217 code like USD, INR, or null),
headcount_growth_percentage (number, e.g. 20 for 20%, or null),
key_product_launch (short string or null).
Use null when the article doesn't say. Never guess."""

def extract(text: str, previous: dict | None = None, errors: list[str] | None = None) -> dict:
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": f"ARTICLE:\n{text}"}]
    if errors:
        messages += [
            {"role": "assistant", "content": json.dumps(previous)},
            {"role": "user", "content":
             "Your previous output failed validation:\n- " + "\n- ".join(errors) +
             "\nFix ONLY these fields and return the full corrected JSON."},
        ]
    resp = client.chat.completions.create(
        model=MODEL, messages=messages, temperature=0,
    )
    return json.loads(resp.choices[0].message.content)