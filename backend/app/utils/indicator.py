import re

def detect_indicator_type(value: str):
    value = value.strip()

    # IP address
    ip_pattern = r"^(?:\d{1,3}\.){3}\d{1,3}$"
    if re.match(ip_pattern, value):
        return "ip"

    # URL
    if value.startswith("http://") or value.startswith("https://"):
        return "url"

    # Domain
    domain_pattern = r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(domain_pattern, value):
        return "domain"

    # Hash (SHA256)
    if len(value) == 64:
        return "hash"

    return "unknown"
