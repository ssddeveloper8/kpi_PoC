from fastapi import FastAPI, Body
import re

from db.connection import get_connections
from llm.llm_client import parse_query_with_llm
from kpi.kpi_service import handle_kpi_query, handle_relative_dates
from kpi.kpi_parser import extract_kpi_name_fallback
from tag.tag_service import handle_tag_query
from tag.tag_parser import extract_tag_name_fallback

app = FastAPI()

connections = get_connections()

def split_entities(value):
    if not value:
        return []

    if isinstance(value, list):
        return value

    value = re.sub(r"(average|max|min|kpi|tag|of)", "", value, flags=re.IGNORECASE)

    parts = re.split(r",| and ", value)

    return [p.strip() for p in parts if p.strip()]

def is_compare_query(query: str):
    return any(word in query.lower() for word in ["compare", "vs", "versus"])

@app.post("/ask")
def ask_api(query: str = Body(..., media_type="text/plain")):

    parsed = parse_query_with_llm(query)
    parsed["raw_query"] = query

    if "tag" in query.lower():
        parsed["kpi_name"] = None

    if "kpi" in query.lower():
        parsed["tag_name"] = None

    kpi_list = split_entities(parsed.get("kpi_name"))

    if not kpi_list:
        fallback = extract_kpi_name_fallback(query)
        kpi_list = [fallback] if fallback else []

    tag_list = split_entities(parsed.get("tag_name"))

    if not tag_list:
        fallback_tag = extract_tag_name_fallback(query)
        tag_list = [fallback_tag] if fallback_tag else []

    if not kpi_list and not tag_list:
        return {"error": "No KPI or TAG detected"}

    parsed = handle_relative_dates(parsed)

    compare_mode = is_compare_query(query)

    results = {}
    comparison = {}

    for kpi in kpi_list:
        if not kpi:
            continue

        parsed["kpi_name"] = kpi
        result = handle_kpi_query(parsed, connections)

        if compare_mode:
            comparison[f"kpi:{kpi}"] = result
        else:
            results[f"kpi:{kpi}"] = result

    for tag in tag_list:
        if not tag:
            continue

        parsed["tag_name"] = tag
        result = handle_tag_query(parsed, connections)

        if compare_mode:
            comparison[f"tag:{tag}"] = result
        else:
            results[f"tag:{tag}"] = result

    if compare_mode:
        return {
            "query": query,
            "comparison": comparison
        }

    return {
        "query": query,
        "results": results
    }