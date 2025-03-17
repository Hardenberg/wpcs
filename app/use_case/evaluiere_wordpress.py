from ..models import DNS, Wordpress, Http
from django.db.models import Count
import socket
import requests
import re

# def check_Wordpress():
#     return {
#         'version': ''
#     }

def check_Wordpress(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        match = re.search(r'<meta name="generator" content="WordPress ([\d.]+)"', response.text)
        return match.group(1) if match else '-'
    
    except requests.RequestException as e:
        return f'-'

def execute():
    working_list = DNS.objects.filter(wordpress__isnull=True, http__https = True)[:100]
    for item in working_list:
        hostname = 'https://'+ item.dns + '.'+ item.tld
        checked = check_Wordpress(hostname)
     
        wordpress, created = Wordpress.objects.get_or_create(
            version=checked,
            dnsId_id=item.id
        )   
        if not created:
            wordpress.version = checked
            wordpress.save
