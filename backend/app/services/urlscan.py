import requests

URLSCAN_API = "https://urlscan.io/api/v1/scan/"
HEADERS = {
    "Content-Type": "application/json"
}

def query_urlscan(url: str):
    payload = {
        "url": url,
        "visibility": "public"
    }

    response = requests.post(URLSCAN_API, headers=HEADERS, json=payload, timeout=15)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "urlscan request failed"
        }

    data = response.json()

    return {
        "status": "submitted",
        "scan_id": data.get("uuid"),
        "result_url": data.get("result")
    }
