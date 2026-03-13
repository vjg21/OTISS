from app.services.securitytrails import query_securitytrails

def get_passive_dns(domain: str):
    data = query_securitytrails(domain)

    if not data:
        return {
            "domain": domain,
            "subdomains": 0,
            "ips": [],
            "source": "securitytrails"
        }

    return {
        "domain": domain,
        "subdomains": len(data.get("subdomains", [])),
        "ips": data.get("ips", []),
        "source": "securitytrails"
    }
