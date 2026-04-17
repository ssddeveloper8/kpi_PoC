import requests
from config import OLLAMA_URL, MODEL_NAME
import json


def parse_query_with_llm(query: str):
    prompt = f"""
Extract structured info STRICTLY.

Rules:
- If multiple KPIs or TAGs are present, return them as a LIST
- Do NOT merge names into one string
- aggregation must be one of: avg, max, min, latest
- If query has "kpi", fill only kpi_name
- If query has "tag", fill only tag_name
- Return ONLY JSON (no explanation)

Return JSON:
{{
  "kpi_name": ["kpi1", "kpi2"] OR null,
  "tag_name": ["tag1", "tag2"] OR null,
  "aggregation": ["avg","min","max"] OR ["avg"] OR ["latest"],
  "start_date": null,
  "end_date": null
}}

Query: {query}
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