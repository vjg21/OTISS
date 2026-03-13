import os
import requests

ST_API_KEY = os.getenv("SECURITYTRAILS_API_KEY")
ST_BASE = "https://api.securitytrails.com/v1"

def query_securitytrails(domain: str):
    if not ST_API_KEY:
        return None

    headers = {
        "APIKEY": ST_API_KEY
    }

    try:
        r = requests.get(
            f"{ST_BASE}/domain/{domain}",
            headers=headers,
            timeout=10
        )

        if r.status_code != 200:
            return None

        return r.json()

    except:
        return None
