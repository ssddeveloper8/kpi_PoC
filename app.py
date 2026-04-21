from fastapi import FastAPI, Body

from db.connection import get_connections
from core.llm import parse_query
from core.entity import detect_entity, split_entities
from core.intent import detect_intent
from core.query_engine import handle_query

from utils.aggregation import normalize_agg, extract_agg_from_query
from utils.date_utils import handle_relative_dates

app = FastAPI()
connections = get_connections()


@app.post("/ask")
def ask(query: str = Body(...)):

    parsed = parse_query(query)
    parsed["raw_query"] = query

    entity_type, names = detect_entity(parsed, query)

    if not entity_type:
        return {"error": "No entity detected"}

    names = split_entities(names)
    names = [n.strip() for n in names if n.strip()]

    parsed = handle_relative_dates(parsed)

    llm_agg = normalize_agg(parsed.get("aggregation"))
    rule_agg = extract_agg_from_query(query)

    agg = rule_agg if rule_agg else llm_agg

    if not agg:
        agg = ["latest"]
        
    if not agg:
        agg = ["latest"]

    intent = detect_intent(parsed, query)

    result = handle_query(parsed, connections, entity_type, names, agg, intent)

    response = {
        "query": query,
        "entity": entity_type,
        "intent": intent,
        "results": result
    }

    if parsed.get("start_date") or parsed.get("end_date"):
        response["date_range"] = {
            "start_date": parsed.get("start_date"),
            "end_date": parsed.get("end_date")
        }

    print("Parsed:", parsed)
    print("Names:", names)
    print("Agg:", agg)
    print("Intent:", intent)

    return response