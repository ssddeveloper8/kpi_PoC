import psycopg2
from config import DATABASES


def get_connections():
    conns = {}

    for name, cfg in DATABASES.items():
        conns[name] = psycopg2.connect(
            host=cfg["host"],
            dbname=cfg["dbname"],
            user=cfg["user"],
            password=cfg["password"],
            port=cfg["port"]
        )

    return conns