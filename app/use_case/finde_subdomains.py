import socket

from ..models import DNS, SubdomainsTop100Liste, TLD, SubDomains
import logging

logger = logging.getLogger(__name__)

def check_subdomain(dns, subdomain, tld):
    try:
        url = subdomain+ '.'+ dns + '.' + tld
        ip_address = socket.gethostbyname(url)
        if ip_address:
            return {
                "valid": True,
                "dns": dns,
                "tld": tld,
                "subdomain": subdomain,
                "ip": ip_address
            }
        
    except Exception as e:
        return {
            "valid": False,
            "dns": dns,
            "tld": tld,
            "subdomain": subdomain,
            "ip": None,
            "error": str(e)
        }

def execute():
    working_list = DNS.objects.filter(subdomains__isnull=True, http__https=True, has_subdomains__isnull=True)[:5]

    logger.info(f'{len(working_list)} DNS-Einträge werden auf Subdomains geprüft')

    for item in working_list:
        try:
            tld = TLD.objects.get(tld=item.tld)
            subdomains = SubdomainsTop100Liste.objects.filter(tld=tld)

            found_subdomains = []
            for subdomain in subdomains:
                checked = check_subdomain(item.dns, subdomain.sub, tld.tld)
                if checked['valid']:
                    found_subdomains.append(
                        SubDomains(dnsId_id=item.id, subdomain=subdomain.sub, ip=checked['ip'])
                    )

            if len(found_subdomains)< 100 and len(found_subdomains) > 0:
                SubDomains.objects.bulk_create(found_subdomains)
                item.has_subdomains = True
            else:
                item.has_subdomains = False

            item.save()

        except Exception as e:
            logger.error(f'Fehler beim Verarbeiten von {item.dns}: {e}', exc_info=True) 