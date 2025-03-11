from ..models import DNS, Wordpress, Http
import socket
import requests
import re

def check_security_txt(domain):
    paths = ["/.well-known/security.txt", "/security.txt"]
    protocols = ["https"]
    
    for protocol in protocols:
        for path in paths:
            url = f"{protocol}://{domain}{path}"
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    return url
                
            except requests.RequestException as e:
                continue
    return '-'
def execute():
    working =Http.objects.filter(security_txt= None)[:20]
    for item in working:
        hostname = item.dnsId.hostname()
        url = check_security_txt(hostname)
        if (url == '-'):
            item.has_security_txt = False
        else:
            item.has_security_txt = True
        item.security_txt = url
        item.save()