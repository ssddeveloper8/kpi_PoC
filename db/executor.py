import math

def clean_nan(obj):
    if isinstance(obj, float) and math.isnan(obj):
        return None
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_nan(i) for i in obj]
    return obj


def execute_sql(conn, sql):
    cursor = conn.cursor()

    try:
        cursor.execute(sql)

        if cursor.description:
            cols = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()

            result = [dict(zip(cols, r)) for r in rows]

            return clean_nan(result) 

        return []

    except Exception as e:
        conn.rollback()
        return {"error": str(e)}

    finally:
        cursor.close()