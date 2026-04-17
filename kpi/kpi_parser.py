def extract_kpi_name_fallback(query: str):
    words = query.split()

    for i, w in enumerate(words):
        if w.lower() == "kpi" and i + 1 < len(words):
            return words[i + 1]

    return None
