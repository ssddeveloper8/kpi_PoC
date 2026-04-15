from fastapi import FastAPI, Body

from db.connection import get_connections
from llm.llm_client import parse_query_with_llm
from kpi.kpi_service import handle_kpi_query, handle_relative_dates
from kpi.kpi_parser import extract_kpi_name_fallback

app = FastAPI()

connections = get_connections()


@app.post("/ask")
def ask_api(query: str = Body(..., media_type="text/plain")):

    parsed = parse_query_with_llm(query)

    # store raw query
    parsed["raw_query"] = query

    # fallback KPI detection
    if not parsed.get("kpi_name"):
        parsed["kpi_name"] = extract_kpi_name_fallback(query)

    if not parsed["kpi_name"]:
        return {"error": "KPI not detected"}

    # handle time logic
    parsed = handle_relative_dates(parsed)

    result = handle_kpi_query(parsed, connections)

    return {
        "query": query,
        "result": result
    }
