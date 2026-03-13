from app.database import get_connection

def is_trusted_indicator(indicator: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT source FROM trusted_indicators WHERE indicator = %s",
        (indicator,)
    )

    row = cur.fetchone()
    conn.close()

    if row:
        return True, row[0]

    return False, None

