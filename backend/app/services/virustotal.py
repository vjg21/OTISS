import os
import requests

VT_API_KEY = os.getenv("VT_API_KEY")
VT_BASE = "https://www.virustotal.com/api/v3"

def query_virustotal(indicator: str, indicator_type: str):
    if not VT_API_KEY:
        return None

    headers = {"x-apikey": VT_API_KEY}

    if indicator_type == "hash":
        url = f"{VT_BASE}/files/{indicator}"

    elif indicator_type == "ip":
        url = f"{VT_BASE}/ip_addresses/{indicator}"

    elif indicator_type == "url":
        return submit_and_fetch_url(indicator, headers)

    else:
        return None

    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None


def submit_and_fetch_url(target_url, headers):
    try:
        r = requests.post(
            f"{VT_BASE}/urls",
            headers=headers,
            data={"url": target_url},
            timeout=15
        )
        if r.status_code not in (200, 202):
            return None

        analysis_id = r.json()["data"]["id"]

        r2 = requests.get(
            f"{VT_BASE}/analyses/{analysis_id}",
            headers=headers,
            timeout=15
        )
        if r2.status_code != 200:
            return None

        return r2.json()
    except:
        return None
