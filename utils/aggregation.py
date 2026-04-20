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
        "mean": "avg",
        "maximum": "max",
        "minimum": "min",
        "sum": "sum",
        "total": "sum",
        "overall": "sum"
    }

    return [mapping.get(a.lower(), a.lower()) for a in agg]


def build_select_clause(agg_list):
    return [AGG_MAP[a] for a in agg_list if a in AGG_MAP]