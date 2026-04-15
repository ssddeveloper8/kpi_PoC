import requests
from config import OLLAMA_URL, MODEL_NAME
import json

def parse_query_with_llm(query: str):
    prompt = f"""
Extract structured info from user query.

STRICT:
- Extract KPI name EXACTLY as written
- NEVER skip KPI name
- Output valid JSON only

STRICT RULES:
- Dates MUST be in YYYY-MM-DD format
- If "last 7 days" → calculate actual dates
- If "last 1 month" → calculate exact start/end date
- If "today" → use today's date
- DO NOT return text like "(today - 30 days)"

Return JSON ONLY:
{{
  "kpi_name": "...",
  "aggregation": "avg/max/min/latest",
  "start_date": "YYYY-MM-DD or null",
  "end_date": "YYYY-MM-DD or null"
}}

Query:
{query}
"""

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    })

    text = response.json()["response"]

    try:
        return json.loads(text)
    except:
        return {
            "kpi_name": None,
            "aggregation": "latest",
            "start_date": None,
            "end_date": None
        }