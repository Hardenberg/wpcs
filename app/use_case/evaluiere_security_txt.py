from ..models import DNS, Wordpress, Http
import requests
import logging
logger = logging.getLogger('django')
def check_security_txt(domain):
    paths = ["/.well-known/security.txt", "/security.txt"]
    protocols = ["https", "http"]
    
    for protocol in protocols:
        for path in paths:
            url = f"{protocol}://{domain}{path}"
            try:
                response = requests.get(url, timeout=10, allow_redirects=True)
                if response.status_code in [200, 301, 302]:  # Auch Weiterleitungen zulassen
                    return url
            except requests.RequestException:
                continue
    return '-'

def execute():
    working = Http.objects.filter(security_txt=None).select_related("dnsId")
    to_update = []
    logger.info(len(working))
    for item in working:
        if item.dnsId:
            hostname = item.dnsId.hostname()
            url = check_security_txt(hostname)
            item.has_security_txt = url != '-'
            item.security_txt = url
            to_update.append(item)

    if to_update:
        logger.info(f"Update {len(to_update)} security")
        Http.objects.bulk_update(to_update, ['has_security_txt', 'security_txt'])
