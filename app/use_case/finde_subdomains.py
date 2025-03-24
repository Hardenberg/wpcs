import socket

from ..models import DNS, SubdomainsTop100Liste, TLD, SubDomains

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
    working_list = DNS.objects.filter(subdomains__isnull=True, http__https=True, has_subdomains=None)[:5]
    
    print(str(len(working_list)) + ' DNS to check for subdomains')
    for item in working_list:
        tld = TLD.objects.filter(tld=item.tld).first()
        subdomains = SubdomainsTop100Liste.objects.filter(tld=tld.id)
        result = 0
        for subdomain in subdomains:
            checked = check_subdomain(item.dns, subdomain.sub, tld.tld)
            if checked['valid']  == True:
                SubDomains.objects.get_or_create(dnsId_id=item.id, subdomain=subdomain.sub, ip=checked['ip'])
                result = result + 1
        if result > 0:
            item.has_subdomains = True
        else:
            item.has_subdomains = False
        item.save()        