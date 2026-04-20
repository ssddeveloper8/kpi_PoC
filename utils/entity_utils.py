import re

def split_entities(value):
    if not value:
        return []

    if isinstance(value, list):
        return value

    value = re.sub(r"(average|max|min|kpi|tag|of)", "", value, flags=re.IGNORECASE)
    parts = re.split(r",| and ", value)

    return [p.strip() for p in parts if p.strip()]


def detect_entity(parsed, query: str):
    if parsed.get("kpi_name"):
        return "kpi", parsed["kpi_name"]

    if parsed.get("tag_name"):
        return "tag", parsed["tag_name"]

    q = query.lower()

    if "kpi" in q:
        return "kpi", []
    if "tag" in q:
        return "tag", []

    return None, []

def is_details_query(query: str):
    keywords = ["details", "info", "information", "metadata"]
    return any(k in query.lower() for k in keywords)


def is_aggregation_query(parsed):
    agg = parsed.get("aggregation")

    if not agg:
        return False

    if isinstance(agg, str):
        agg = [agg]

    return any(a in ["avg", "max", "min", "sum"] for a in agg)


def detect_attribute(query: str):
    query = query.lower()

    if "cart id" in query:
        return "cart_id"
    if "tag id" in query:
        return "tag_id"
    if "alise" in query:
        return "alise"

    return None


def is_count_query(query: str):
    return "how many" in query.lower()