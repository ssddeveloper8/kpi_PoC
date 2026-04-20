from db.executor import execute_sql
from utils.aggregation import build_select_clause


def get_metadata(conn, table, name_field, value):
    sql = f"""
    SELECT *
    FROM {table}
    WHERE LOWER({name_field}) LIKE LOWER('%{value}%')
    LIMIT 1;
    """
    return execute_sql(conn, sql)


def get_all_metadata(conn, table):
    sql = f"""
    SELECT *
    FROM {table}
    LIMIT 50;
    """
    return execute_sql(conn, sql)


def get_values(conn, config, entity_id, agg_list, time_filter):
    table = config["value_table"]
    id_field = config["id_field"]

    where_clause = f"{id_field} = '{entity_id}'"

    if config.get("extra_condition"):
        where_clause += f" AND {config['extra_condition']}"

    if time_filter:
        where_clause += f" AND {time_filter}"

    select_parts = build_select_clause(agg_list)

    if not select_parts:
        sql = f"""
        SELECT value, to_timestamp(epoch_seconds) as timestamp
        FROM {table}
        WHERE {where_clause}
        ORDER BY epoch_seconds DESC
        LIMIT 1;
        """
        return execute_sql(conn, sql)

    sql = f"""
    SELECT {", ".join(select_parts)}
    FROM {table}
    WHERE {where_clause};
    """
    return execute_sql(conn, sql)