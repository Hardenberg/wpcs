import requests
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.db import transaction
from ..models import DNS, Wordpress
import logging
logger = logging.getLogger('django')

def check_wordpress(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        match = re.search(r'<meta name="generator" content="WordPress ([\d.]+)"', response.text)
        return match.group(1) if match else '-'
    
    except requests.RequestException:
        return '-'

def process_dns_entry(item_id):
    with transaction.atomic():  # Sperrt die Zeile exklusiv
        item = DNS.objects.select_for_update(skip_locked=True).get(id=item_id)
        
        if Wordpress.objects.filter(dnsId_id=item.id).exists():  # Doppelprüfungen vermeiden
            return item.id, None  

        hostname = f"https://{item.dns}.{item.tld}"
        version = check_wordpress(hostname)

        Wordpress.objects.create(dnsId_id=item.id, version=version)
    
    return item.id, version

def execute():
    working_list = DNS.objects.filter(wordpress__isnull=True, http__https=True).values_list("id", flat=True)
    logger.info(str(len(working_list)) + ' DNS to check')
    with ThreadPoolExecutor(max_workers=1) as executor:  # 10 gleichzeitige Threads
        future_to_item = {executor.submit(process_dns_entry, item_id): item_id for item_id in working_list}

        for future in as_completed(future_to_item):
            item_id, version = future.result()
            if version and version != '-':
                logger.info(f"DNS-ID {item_id} → WordPress-Version: {version}")
