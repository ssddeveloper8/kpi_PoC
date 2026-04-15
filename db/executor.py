def execute_sql(conn, sql):
    cursor = conn.cursor()

    try:
        cursor.execute(sql)

        if cursor.description:
            cols = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(cols, r)) for r in rows]

        return []

    except Exception as e:
        conn.rollback()
        return {"error": str(e)}

    finally:
        cursor.close()