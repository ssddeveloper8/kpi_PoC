from entity_config import ENTITY_CONFIG
from db.executor import execute_sql
from utils.aggregation import build_select_clause
from utils.date_utils import build_time_filter


def get_metadata(conn, table, field, value):
    sql = f"""
    SELECT *
    FROM {table}
    WHERE LOWER({field}) LIKE LOWER('%{value}%')
    LIMIT 1;
    """
    return execute_sql(conn, sql)


def get_values(conn, config, entity_id, agg, time_filter):
    table = config["value_table"]
    id_field = config["id_field"]

    where = f"{id_field} = '{entity_id}'"

    if config.get("extra_condition"):
        where += f" AND {config['extra_condition']}"

    if time_filter:
        where += f" AND {time_filter}"

    select = build_select_clause(agg)

    if not select:
        sql = f"""
        SELECT value, to_timestamp(epoch_seconds) as timestamp
        FROM {table}
        WHERE {where}
        ORDER BY epoch_seconds DESC
        LIMIT 1;
        """
    else:
        sql = f"""
        SELECT {", ".join(select)}
        FROM {table}
        WHERE {where};
        """

    return execute_sql(conn, sql)


def handle_query(parsed, connections, entity_type, names, agg, intent):
    config = ENTITY_CONFIG[entity_type]

    if intent == "count":
        sql = f"SELECT COUNT(*) as count FROM {config['meta_table']}"
        return execute_sql(connections["builder"], sql)

    results = {}

    for name in names:
        meta = get_metadata(
            connections["builder"],
            config["meta_table"],
            config["meta_name_field"],
            name
        )

        if not meta:
            results[name] = {"error": "Not found"}
            continue

        if intent == "attribute":
            attr = parsed.get("attribute")
            col = config["attributes"].get(attr)
            results[name] = [{attr: meta[0].get(col)}]
            continue

        if intent == "details":
            results[name] = meta
            continue

        entity_id = meta[0][config["id_column"]]

        values = get_values(
            connections["historian"],
            config,
            entity_id,
            agg,
            build_time_filter(parsed.get("start_date"), parsed.get("end_date"))
        )

        results[name] = values

    return results