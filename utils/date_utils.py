from datetime import datetime, timedelta
import re

def safe_parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return None

def build_time_filter(start_date, end_date):
    conditions = []

    start_dt = safe_parse_date(start_date) if start_date else None
    end_dt = safe_parse_date(end_date) if end_date else None

    if start_dt:
        conditions.append(f"epoch_seconds >= {int(start_dt.timestamp())}")

    if end_dt:
        conditions.append(f"epoch_seconds <= {int(end_dt.timestamp())}")

    return " AND ".join(conditions)


def handle_relative_dates(parsed):
    today = datetime.today()
    query = parsed.get("raw_query", "").lower()

    match = re.search(r"last (\d+) days?", query)
    if match:
        d = int(match.group(1))
        parsed["start_date"] = (today - timedelta(days=d)).strftime("%Y-%m-%d")
        parsed["end_date"] = today.strftime("%Y-%m-%d")

    return parsed