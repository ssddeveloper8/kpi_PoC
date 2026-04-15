import requests
from config import OLLAMA_URL, MODEL_NAME
import json


def parse_query_with_llm(query: str):
    prompt = f"""
Extract structured info.

Return JSON:
{{
  "kpi_name": "...",
  "aggregation": ["avg","max","min"] OR ["avg"] OR ["latest"],
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