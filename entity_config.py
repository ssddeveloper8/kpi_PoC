ENTITY_CONFIG = {
    "kpi": {
        "meta_table": "tbl_kpi_engine_kpi_calculation",
        "meta_name_field": "kpi_name",
        "value_table": "tbl_kpi_historian_data",
        "id_column": "alise",
        "id_field": "alise",
        "attributes": {
            "cart_id": "cart_id",
            "alise": "alise"
        }
    },
    "tag": {
        "meta_table": "tbl_cfg_opc_hda_tag_config",
        "meta_name_field": "tag_name",
        "value_table": "tbl_tag_historian_data",
        "id_column": "tag_id",
        "id_field": "tag_id",
        "extra_condition": """
            value IS NOT NULL
            AND value::text != 'NaN'
            AND value::text != 'Infinity'
            AND value::text != '-Infinity'
        """,
        "attributes": {
            "tag_id": "tag_id"
        }
    }
}