import os
import requests
from urllib.parse import quote

OTX_BASE = "https://otx.alienvault.com/api/v1"

def query_otx(indicator: str, indicator_type: str):
    api_key = os.getenv("OTX_API_KEY")

    # If API key missing → skip safely
    if not api_key:
        return None

    headers = {
        "X-OTX-API-KEY": api_key
    }

    try:
        if indicator_type == "ip":
            url = f"{OTX_BASE}/indicators/IPv4/{indicator}/general"

        elif indicator_type == "domain":
            url = f"{OTX_BASE}/indicators/domain/{indicator}/general"

        elif indicator_type == "url":
            encoded = quote(indicator, safe="")
            url = f"{OTX_BASE}/indicators/url/{encoded}/general"

        elif indicator_type == "hash":
            url = f"{OTX_BASE}/indicators/file/{indicator}/general"

        else:
            return None

        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            return None

        return r.json()

    except Exception:
        return None
