import dns.resolver

def lookup_dns(domain: str):
    result = {
        "domain": domain,
        "mx": [],
        "txt": []
    }

    # MX records
    try:
        answers = dns.resolver.resolve(domain, "MX")
        for rdata in answers:
            result["mx"].append(str(rdata.exchange).rstrip("."))
    except Exception:
        pass

    # TXT records
    try:
        answers = dns.resolver.resolve(domain, "TXT")
        for rdata in answers:
            result["txt"].append("".join(s.decode() for s in rdata.strings))
    except Exception:
        pass

    return result
