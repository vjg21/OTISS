import requests

API_URL = "http://127.0.0.1:8000/analyze"

def analyze_url(url):
    payload = {
        "indicator": url
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": str(e)
        }

if __name__ == "__main__":
    while True:
        url = input("\nEnter URL to analyze (or 'exit'): ").strip()

        if url.lower() == "exit":
            break

        result = analyze_url(url)

        print("\n--- Analysis Result ---")
        for k, v in result.items():
            print(f"{k}: {v}")
