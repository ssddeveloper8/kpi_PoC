def detect_intent(parsed, query):
    q = query.lower()
    intent = parsed.get("intent")

    if intent:
        intent = intent.lower()

        if intent in ["count", "how many"]:
            return "count"
        if intent in ["attribute"]:
            return "attribute"
        if intent in ["details"]:
            return "details"
        if intent in ["compare", "aggregation"]:
            return "aggregation"

    if "how many" in q:
        return "count"
    if any(x in q for x in ["cart id", "tag id", "alise"]):
        return "attribute"
    if "details" in q:
        return "details"
    if "compare" in q:
        return "aggregation"

    return "aggregation"