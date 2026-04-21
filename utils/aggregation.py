import re

AGG_MAP = {
    "avg": "COALESCE(AVG(value), 0) AS avg_value",
    "max": "COALESCE(MAX(value), 0) AS max_value",
    "min": "COALESCE(MIN(value), 0) AS min_value",
    "sum": "COALESCE(SUM(value), 0) AS sum_value"
}

def normalize_agg(agg):
    if not agg:
        return ["latest"]

    if isinstance(agg, str):
        agg = [agg]

    mapping = {
        "average": "avg",
        "avg": "avg",
        "mean": "avg",
        "sum": "sum",
        "total": "sum",
        "minimum": "min",
        "min": "min",
        "maximum": "max",
        "max": "max"
    }

    result = []

    for a in agg:
        a = a.lower()

        parts = re.split(r",|and", a)

        for p in parts:
            p = p.strip()
            if p in mapping:
                result.append(mapping[p])

    return list(set(result)) or ["latest"]


def build_select_clause(agg_list):
    return [AGG_MAP[a] for a in agg_list if a in AGG_MAP]

def extract_agg_from_query(query: str):
    q = query.lower()

    agg = []

    if "average" in q or "avg" in q:
        agg.append("avg")
    if "sum" in q or "total" in q:
        agg.append("sum")
    if "minimum" in q or "min" in q:
        agg.append("min")
    if "maximum" in q or "max" in q:
        agg.append("max")

    return agg