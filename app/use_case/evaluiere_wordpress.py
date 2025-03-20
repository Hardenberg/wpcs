import requests
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.db import transaction
from ..models import DNS, Wordpress

def check_wordpress(url):
    """
    Prüft, ob die gegebene URL eine WordPress-Seite ist und gibt die Version zurück.
    
    Args:
        url (str): Die URL der zu prüfenden Seite.

    Returns:
        str: WordPress-Version oder '-' falls nicht gefunden.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        match = re.search(r'<meta name="generator" content="WordPress ([\d.]+)"', response.text)
        return match.group(1) if match else '-'
    
    except requests.RequestException:
        return '-'

def process_dns_entry(item_id):
    """
    Prüft eine einzelne DNS-Instanz auf eine WordPress-Installation und speichert das Ergebnis.

    Args:
        item_id (int): Die ID des DNS-Objekts aus der Datenbank.

    Returns:
        tuple: (DNS-Objekt-ID, WordPress-Version)
    """
    with transaction.atomic():  # Sperrt die Zeile exklusiv
        item = DNS.objects.select_for_update(skip_locked=True).get(id=item_id)
        
        if Wordpress.objects.filter(dnsId_id=item.id).exists():  # Doppelprüfungen vermeiden
            return item.id, None  

        hostname = f"https://{item.dns}.{item.tld}"
        version = check_wordpress(hostname)

        # WordPress-Eintrag erstellen
        Wordpress.objects.create(dnsId_id=item.id, version=version)
    
    return item.id, version

def execute():
    """
    Prüft parallel Domains auf WordPress-Installationen, ohne doppelte Prüfungen.
    """
    working_list = DNS.objects.filter(wordpress__isnull=True, http__https=True).values_list("id", flat=True)[:100]
    print(str(len(working_list)) + ' DNS to check')
    with ThreadPoolExecutor(max_workers=1) as executor:  # 10 gleichzeitige Threads
        future_to_item = {executor.submit(process_dns_entry, item_id): item_id for item_id in working_list}

        for future in as_completed(future_to_item):
            item_id, version = future.result()
            if version:
                print(f"DNS-ID {item_id} → WordPress-Version: {version}")
