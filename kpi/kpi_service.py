from db.executor import execute_sql
from datetime import datetime, timedelta
import re


def get_kpi_metadata(conn, kpi_name):
    sql = f"""
    SELECT *
    FROM tbl_kpi_engine_kpi_calculation
    WHERE LOWER(kpi_name) = LOWER('{kpi_name}')
    LIMIT 1;
    """
    return execute_sql(conn, sql)


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


def get_kpi_values(conn, alias, agg, start_date=None, end_date=None):

    time_filter = build_time_filter(start_date, end_date)

    where_clause = f"alise = '{alias}'"

    if time_filter:
        where_clause += f" AND {time_filter}"

    if agg == "avg":
        sql = f"""
        SELECT 
            COUNT(value) as total_points,
            AVG(value) as avg_value
        FROM tbl_current_kpi_historian_data
        WHERE {where_clause};
        """

    elif agg == "max":
        sql = f"""
        SELECT MAX(value) as value
        FROM tbl_current_kpi_historian_data
        WHERE {where_clause};
        """

    elif agg == "min":
        sql = f"""
        SELECT MIN(value) as value
        FROM tbl_current_kpi_historian_data
        WHERE {where_clause};
        """

    else:
        sql = f"""
        SELECT 
            value,
            to_timestamp(epoch_seconds) as timestamp
        FROM tbl_current_kpi_historian_data
        WHERE {where_clause}
        ORDER BY epoch_seconds DESC
        LIMIT 1;
        """

    return execute_sql(conn, sql)


def handle_relative_dates(parsed):
    today = datetime.today()
    query = parsed.get("raw_query", "").lower()

    days_match = re.search(r"last (\d+) days?", query)
    if days_match:
        days = int(days_match.group(1))
        parsed["start_date"] = (today - timedelta(days=days)).strftime("%Y-%m-%d")
        parsed["end_date"] = today.strftime("%Y-%m-%d")
        return parsed

    months_match = re.search(r"last (\d+) months?", query)
    if months_match:
        months = int(months_match.group(1))
        parsed["start_date"] = (today - timedelta(days=30 * months)).strftime("%Y-%m-%d")
        parsed["end_date"] = today.strftime("%Y-%m-%d")
        return parsed

    date_match = re.search(r"(\d{2}-\d{2}-\d{4})", query)
    if date_match:
        d = datetime.strptime(date_match.group(1), "%d-%m-%Y")
        parsed["start_date"] = d.strftime("%Y-%m-%d")
        parsed["end_date"] = d.strftime("%Y-%m-%d")
        return parsed

    if "today" in query:
        parsed["start_date"] = today.strftime("%Y-%m-%d")
        parsed["end_date"] = today.strftime("%Y-%m-%d")

    return parsed


def handle_kpi_query(parsed, connections):
    kpi_name = parsed["kpi_name"]
    agg = parsed["aggregation"]
    start_date = parsed.get("start_date")
    end_date = parsed.get("end_date")

    meta = get_kpi_metadata(connections["builder"], kpi_name)

    if not meta:
        return {"error": "KPI not found"}

    alias = meta[0].get("alise")

    values = get_kpi_values(
        connections["historian"],
        alias,
        agg,
        start_date,
        end_date
    )

    return {
        "kpi_info": meta,
        "kpi_result": values,
        "aggregation": agg,
        "date_range": {
            "start": start_date,
            "end": end_date
        }
    }
