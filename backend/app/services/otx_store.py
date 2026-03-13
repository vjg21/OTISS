from app.database import get_connection

def store_otx(indicator, indicator_type, pulse_count):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO otx_iocs (indicator, indicator_type, pulse_count, reputation)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (indicator)
        DO UPDATE SET
            pulse_count = EXCLUDED.pulse_count,
            last_seen = NOW();
        """,
        (
            indicator,
            indicator_type,
            pulse_count,
            "malicious" if pulse_count > 0 else "clean"
        )
    )

    conn.commit()
    cur.close()
    conn.close()
