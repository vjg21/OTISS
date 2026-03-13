import requests

URLHAUS_API = "https://urlhaus-api.abuse.ch/v1/url/"

def check_urlhaus(url: str):
    try:
        response = requests.post(
            URLHAUS_API,
            data={"url": url},
            timeout=10
        )
        data = response.json()

        # URL is malicious ONLY if listed
        if data.get("query_status") == "ok" and data.get("url_status"):
            return {
                "malicious": True,
                "malware_family": data.get("malware"),
                "url_status": data.get("url_status"),
                "source": "URLHaus"
            }

        return {
            "malicious": False,
            "source": "URLHaus"
        }

    except Exception as e:
        return {
            "error": str(e),
            "source": "URLHaus"
        }
