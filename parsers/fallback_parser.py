def extract_name_fallback(query: str, keyword: str):
    words = query.split()

    for i, w in enumerate(words):
        if w.lower() == keyword and i + 1 < len(words):
            return words[i + 1]

    return None