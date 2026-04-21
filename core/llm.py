import requests
import json
from config import OLLAMA_URL, MODEL_NAME


def parse_query(query: str):
    prompt = f"""
Return ONLY JSON:

{{
  "intent": "aggregation | details | attribute | count | compare",
  "kpi_name": ["kpi1"] OR null,
  "tag_name": ["tag1"] OR null,
  "aggregation": ["avg","min","max","sum"] OR ["latest"],
  "attribute": "cart_id | tag_id | alise | null",
  "start_date": null,
  "end_date": null
}}

Query: {query}
"""

    res = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    })

    try:
        return json.loads(res.json()["response"])
    except:
        return {}