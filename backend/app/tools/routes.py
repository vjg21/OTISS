from fastapi import APIRouter

router = APIRouter()

# =========================
# TOOLS CATALOG (STATIC)
# =========================
TOOLS_CATALOG = {
    "Domain & Infrastructure Analysis": [
        {
            "name": "Domain Monitor (nwesterhausen)",
            "description": "Tracks domain registration and DNS changes.",
            "url": "https://github.com/nwesterhausen/domain-monitor"
        },
        {
            "name": "DNSlytics",
            "description": "DNS history and domain relationship analysis.",
            "url": "https://dnslytics.com/"
        },
        {
            "name": "SecurityTrails",
            "description": "Domain, DNS, and infrastructure intelligence.",
            "url": "https://securitytrails.com/"
        }
    ],

    "Email & Domain Spoofing": [
        {
            "name": "MXToolbox",
            "description": "Mail server, DNS, and blacklist analysis.",
            "url": "https://mxtoolbox.com/"
        },
        {
            "name": "Spoofy",
            "description": "SPF, DKIM, and DMARC spoofing checks.",
            "url": "https://github.com/MattKeeley/Spoofy"
        }
    ],

    "OSINT & Reconnaissance": [
        {
            "name": "Namechk",
            "description": "Username presence across platforms.",
            "url": "https://namechk.com/"
        },
        {
            "name": "Holehe",
            "description": "Checks email usage across services (manual use).",
            "url": "https://github.com/megadose/holehe"
        },
        {
            "name": "Ghunt",
            "description": "Google account OSINT (manual use).",
            "url": "https://github.com/mxrch/GHunt"
        }
    ],

    "Email Header Analysis": [
        {
            "name": "Google Messageheader",
            "description": "Analyzes email routing and headers.",
            "url": "https://toolbox.googleapps.com/apps/messageheader/"
        },
        {
            "name": "RFC822 Parser",
            "description": "Parses raw email headers.",
            "url": "https://www.iptrackeronline.com/email-header-analysis.php"
        }
    ],

    "Malware & File Analysis": [
        {
            "name": "VirusTotal",
            "description": "Multi-engine malware and URL analysis.",
            "url": "https://www.virustotal.com/"
        },
        {
            "name": "Hybrid Analysis",
            "description": "Sandbox malware analysis.",
            "url": "https://www.hybrid-analysis.com/"
        }
    ],

    "Miscellaneous": [
        {
            "name": "Browserling",
            "description": "Cross-browser website testing.",
            "url": "https://www.browserling.com/"
        },
        {
            "name": "ExifTool",
            "description": "Extracts metadata from files and images.",
            "url": "https://exiftool.org/"
        }
    ]
}

# =========================
# TOOLS ENDPOINT
# =========================
@router.get("/")
def list_tools():
    """
    Returns categorized external security tools for analysts.
    """
    return {
        "tool_count": sum(len(v) for v in TOOLS_CATALOG.values()),
        "categories": TOOLS_CATALOG
    }
