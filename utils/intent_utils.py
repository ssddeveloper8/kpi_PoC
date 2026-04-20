def detect_intent(parsed, query: str):
    q = query.lower()

    intent = parsed.get("intent")

    if intent:
        intent = intent.lower()

        if intent in ["count", "how many"]:
            return "count"

        if intent in ["attribute", "field", "column"]:
            return "attribute"

        if intent in ["details", "info", "information"]:
            return "details"

        if intent in ["aggregation", "calculate", "value"]:
            return "aggregation"

        if intent in ["compare", "comparison"]:
            return "aggregation"  


    if "how many" in q or "count" in q:
        return "count"

    if any(x in q for x in ["cart id", "tag id", "alise"]):
        return "attribute"

    if any(x in q for x in ["details", "info", "information"]):
        return "details"

    if any(x in q for x in ["compare", "vs", "versus"]):
        return "aggregation"

    return "aggregation"