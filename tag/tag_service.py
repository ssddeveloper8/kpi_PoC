from db.executor import execute_sql
from datetime import datetime, timedelta
import re


def get_tag_metadata(conn, tag_name):
    sql = f"""
    SELECT *
    FROM tbl_cfg_opc_hda_tag_config
    WHERE LOWER(tag_name) = LOWER('{tag_name}')
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


def normalize_agg(agg):
    if not agg:
        return ["latest"]

    if isinstance(agg, str):
        agg = [agg]

    mapping = {
        "average": "avg",
        "mean": "avg",
        "avg": "avg",
        "maximum": "max",
        "max": "max",
        "minimum": "min",
        "min": "min",
        "latest": "latest"
    }

    return [mapping.get(a.lower(), a.lower()) for a in agg]


def get_tag_values(conn, tag_id, agg_list, start_date=None, end_date=None):

    table_name = "tbl_tag_historian_data"

    time_filter = build_time_filter(start_date, end_date)

    where_clause = f"""
    tag_id = '{tag_id}'
    AND value IS NOT NULL
    AND value::text != 'NaN'
    AND value::text != 'Infinity'
    AND value::text != '-Infinity'
    """

    if time_filter:
        where_clause += f" AND {time_filter}"

    select_parts = []

    if "avg" in agg_list:
        select_parts.append("COALESCE(AVG(value), 0) AS avg_value")

    if "max" in agg_list:
        select_parts.append("COALESCE(MAX(value), 0) AS max_value")

    if "min" in agg_list:
        select_parts.append("COALESCE(MIN(value), 0) AS min_value")

    if not select_parts:
        sql = f"""
        SELECT value, to_timestamp(epoch_seconds) as timestamp
        FROM {table_name}
        WHERE {where_clause}
        ORDER BY epoch_seconds DESC
        LIMIT 1;
        """
        return execute_sql(conn, sql)

    sql = f"""
    SELECT {", ".join(select_parts)}
    FROM {table_name}
    WHERE {where_clause};
    """

    return execute_sql(conn, sql)


def handle_relative_dates(parsed):
    today = datetime.today()
    query = parsed.get("raw_query", "").lower()

    days_match = re.search(r"last (\d+) days?", query)
    if days_match:
        d = int(days_match.group(1))
        parsed["start_date"] = (today - timedelta(days=d)).strftime("%Y-%m-%d")
        parsed["end_date"] = today.strftime("%Y-%m-%d")

    return parsed


def handle_tag_query(parsed, connections):

    tag_name = parsed["tag_name"]

    agg = normalize_agg(parsed.get("aggregation"))

    start_date = parsed.get("start_date")
    end_date = parsed.get("end_date")

    meta = get_tag_metadata(connections["builder"], tag_name)

    if isinstance(meta, dict) and "error" in meta:
        return {
            "error": "Metadata query failed",
            "details": meta["error"]
        }

    if not meta or not isinstance(meta, list):
        return {"error": "Tag not found"}

    tag_id = meta[0].get("tag_id")

    if not tag_id:
        return {"error": "tag_id not found for tag"}

    values = get_tag_values(
        connections["historian"],
        tag_id,
        agg,
        start_date,
        end_date
    )

    is_aggregation = bool(agg and agg != ["latest"])

    if is_aggregation:
        response = {
            "tag_result": values
        }

        if start_date or end_date:
            response["date_range"] = {
                "start": start_date,
                "end": end_date
            }

        return response

    return {
        "tag_info": meta
    }