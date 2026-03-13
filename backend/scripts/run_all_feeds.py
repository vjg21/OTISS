print("[+] Running all OTISS feeds")

from ingest_firehol import ingest_firehol
from ingest_urlhaus import ingest_urlhaus
from ingest_plain_url import ingest_plain_url
from ingest_malwarebazaar import ingest_malwarebazaar
from ingest_nvd import ingest_nvd
from ingest_cisa_kev import ingest_cisa_kev

def main():
    ingest_firehol()
    ingest_urlhaus()
    ingest_plain_url()
    ingest_malwarebazaar()
    ingest_nvd()
    ingest_cisa_kev()
    print("[✓] All feeds updated successfully")

if __name__ == "__main__":
    main()
