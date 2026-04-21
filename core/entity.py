import re

def detect_entity(parsed, query):
    if parsed.get("kpi_name"):
        return "kpi", parsed["kpi_name"]

    if parsed.get("tag_name"):
        return "tag", parsed["tag_name"]

    q = query

    kpi_match = re.findall(r"kpi\s+([A-Za-z0-9_.]+)", q, re.IGNORECASE)
    tag_match = re.findall(r"tag\s+([A-Za-z0-9_.]+)", q, re.IGNORECASE)

    if kpi_match:
        return "kpi", kpi_match

    if tag_match:
        return "tag", tag_match

    if "kpi" in q.lower():
        return "kpi", []
    if "tag" in q.lower():
        return "tag", []

    return None, []


def split_entities(value):
    if not value:
        return []

    if isinstance(value, list):
        return value

    parts = re.split(r",| and ", value)
    return [p.strip() for p in parts if p.strip()]