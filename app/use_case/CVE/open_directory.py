import requests
from urllib.parse import urljoin
from django.db import IntegrityError
from ...models import Wordpress
import textwrap

def check_directory_listing(base_url, file_list, timeout=10):
    for file_name in file_list:
        file_url = urljoin(base_url, file_name)
        
        try:
            response = requests.get(file_url, timeout=timeout)
            if response.status_code >= 200 and response.status_code < 300:
                print(f"Gefunden: {file_url} (Status: {response.status_code})")
                print(textwrap.shorten(response.text, width=100, placeholder="..."))
                if (len(response.text)) > 0:
                    return True
            else:
                continue
        except requests.exceptions.Timeout:
            continue
        except requests.exceptions.RequestException as e:
            continue

    return False  

def resolve_directory(base_url, timeout=10):
    file_list = [
        'wp-config.php',     # Wichtig für Sicherheit
        'uploads/.htaccess',  # .htaccess kann wichtige Sicherheitsregeln enthalten
    ]
    
    return check_directory_listing(base_url, file_list, timeout)

def execute():
    workinglist = Wordpress.objects.filter(open_directory=None).exclude(version='-').select_related('dnsId')
    print(f"{len(workinglist)} WordPress-Instanzen zu prüfen")
    
    updates = []
    for item in workinglist:
        dns = item.dnsId
        hostname = f"https://{dns.dns}.{dns.tld}"
        
        result = resolve_directory(hostname, timeout=10)  
        print(f"Verzeichnisauflösung für {hostname}: {result}")
        
        item.open_directory = result
        updates.append(item)

    if updates:
        try:
            Wordpress.objects.bulk_update(updates, ['open_directory'])
            print(f"Erfolgreich {len(updates)} Einträge aktualisiert.")
        except IntegrityError as e:
            print(f"Fehler beim Aktualisieren der Einträge: {e}")
