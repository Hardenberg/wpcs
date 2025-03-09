from ..models import DNS, Http
import socket

ports = [80, 443] 

def check_open_ports(item):
    
    # Port 443
    port_443 = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # Timeout für die Verbindung setzen
        result = s.connect_ex((item.ip, 443))  # 0 = offen, anderes = geschlossen
        if result == 0:
            port_443 = True

    # Port 80
    port_80 = False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # Timeout für die Verbindung setzen
        result = s.connect_ex((item.ip, 80))  # 0 = offen, anderes = geschlossen
        if result == 0:
            port_80 = True
    result = {
        'item':item,
        '443': port_443,
        '80': port_80
    }

    return result

def execute():
    working_list = DNS.objects.filter(http__isnull=True)[:100]
    for item in working_list:
        open_ports = check_open_ports(item)
        Http.objects.create(
            http=open_ports['80'],
            https=open_ports['443'],
            dnsId=open_ports['item']
        )