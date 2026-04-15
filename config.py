DATABASES = {
    "builder": {
        "host": "localhost",
        "dbname": "Builder DB",
        "user": "postgres",
        "password": "root",
        "port": 5432
    },
    "historian": {
        "host": "localhost",
        "dbname": "Historian DB",
        "user": "postgres",
        "password": "root",
        "port": 5432
    }
}

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"