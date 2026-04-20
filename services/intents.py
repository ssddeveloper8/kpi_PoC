from db.executor import execute_sql
from services.entity_service import get_metadata, get_values, get_all_metadata
from utils.date_utils import build_time_filter
from entity_config import ENTITY_CONFIG


def handle_count(parsed, connections, entity_type, names, agg):
    config = ENTITY_CONFIG[entity_type]

    sql = f"SELECT COUNT(*) AS count FROM {config['meta_table']};"
    return execute_sql(connections["builder"], sql)


def handle_attribute(parsed, connections, entity_type, names, agg):
    config = ENTITY_CONFIG[entity_type]
    attribute = parsed.get("attribute")

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

        column = config["attributes"].get(attribute)
        results[name] = [{attribute: meta[0].get(column)}]

    return results


def handle_details(parsed, connections, entity_type, names, agg):
    config = ENTITY_CONFIG[entity_type]

    results = {}

    for name in names:
        meta = get_metadata(
            connections["builder"],
            config["meta_table"],
            config["meta_name_field"],
            name
        )
        results[name] = meta

    return results


def handle_aggregation(parsed, connections, entity_type, names, agg):
    config = ENTITY_CONFIG[entity_type]

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