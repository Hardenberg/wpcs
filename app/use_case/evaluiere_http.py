from concurrent.futures import ThreadPoolExecutor, as_completed
from django.db import transaction
from ..models import DNS, Http
import socket

ports = [80, 443]

def is_port_open(ip, port, timeout=2):
    """Prüft, ob ein bestimmter Port auf einer IP-Adresse offen ist."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        return s.connect_ex((ip, port)) == 0

def check_open_ports(item):
    """Überprüft, ob die Ports 80 und 443 für eine bestimmte IP-Adresse offen sind."""
    return {
        'item': item,
        '443': is_port_open(item.ip, 443),
        '80': is_port_open(item.ip, 80),
    }

def execute():
    working_list = DNS.objects.filter(http__isnull=True)
    print(f"{len(working_list)} DNS-Einträge zu prüfen.")

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_item = {executor.submit(check_open_ports, item): item for item in working_list}
        
        for future in as_completed(future_to_item):
            open_ports = future.result()
            results.append(Http(
                http=open_ports['80'],
                https=open_ports['443'],
                dnsId=open_ports['item']
            ))

    if results:
        with transaction.atomic():  # Datenbank-Transaktion für bessere Performance
            Http.objects.bulk_create(results)
