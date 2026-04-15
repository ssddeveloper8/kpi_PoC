def parse_kpi_query(query: str):
    q = query.lower()

    is_kpi = "kpi" in q

    words = query.split()
    kpi_name = None

    for i, w in enumerate(words):
        if w.lower() == "kpi" and i + 1 < len(words):
            kpi_name = words[i + 1]

    if "average" in q or "avg" in q:
        agg = "avg"
    elif "max" in q:
        agg = "max"
    elif "min" in q:
        agg = "min"
    else:
        agg = "latest"

    return {
        "is_kpi": is_kpi,
        "kpi_name": kpi_name,
        "agg": agg
    }
    
def extract_kpi_name_fallback(query: str):
    words = query.split()

    for i, w in enumerate(words):
        if w.lower() == "kpi" and i + 1 < len(words):
            return words[i + 1]

    return None