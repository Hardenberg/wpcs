import logging
import requests
from urllib.parse import urljoin
from django.db import IntegrityError
from ...models import Wordpress
import textwrap
import re

logger = logging.getLogger('django')
def is_wp_config(content: str) -> bool:
    wp_keys = [
        "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST",
        "AUTH_KEY", "SECURE_AUTH_KEY", "LOGGED_IN_KEY", "NONCE_KEY"
    ]
    if any(key in content for key in wp_keys):
        return True
    if re.search(r"define\(['\"](DB_[A-Z_]+|AUTH_KEY|SECURE_AUTH_KEY)['\"],\s*['\"].+['\"]\)", content):
        logger.info("wp-config gefunden")
        return True
    return False

def is_htaccess(content: str) -> bool:
    htaccess_keys = [
        "RewriteEngine", "RewriteRule", "RewriteCond", "Options",
        "Deny from", "Allow from", "AuthType", "AuthName",
        "Require", "Order", "Header set", "SetEnvIf"
    ]
    
    if any(key in content for key in htaccess_keys):
        return True

    patterns = [
        r"RewriteEngine\s+(on|off)",            # Aktivierung der Rewrite Engine
        r"RewriteRule\s+\^?.+\s+\S+",           # RewriteRule mit Pfaden
        r"RewriteCond\s+%?\{\w+\}\s+\[?.+\]?",  # RewriteCond mit Variablen
        r"Options\s+(-|\+)?\w+",                # Apache-Optionen setzen
        r"Deny from\s+\S+",                     # Zugriff verweigern
        r"Allow from\s+\S+",                    # Zugriff erlauben
        r"AuthType\s+\w+",                      # Authentifizierungstyp
        r"AuthName\s+\".+?\"",                  # Authentifizierungsname
        r"Require\s+\w+",                       # Zugriffsbeschränkung
        r"Header\s+set\s+\S+",                  # HTTP-Header setzen
        r"SetEnvIf\s+\w+\s+\S+"                 # Umgebungsvariablen setzen
    ]
    
    if any(re.search(pattern, content, re.IGNORECASE) for pattern in patterns):
        logger.info("htaccess gefunden")
        return True

    return False

def check_directory_listing(base_url, file_list, timeout=10):
    for file_name in file_list:
        file_url = urljoin(base_url, file_name)
        
        try:
            head_response = requests.head(file_url, timeout=timeout, allow_redirects=True)
            if head_response.status_code != 200:
                continue  # Datei existiert nicht oder ist nicht erreichb4ar
            
            response = requests.get(file_url, timeout=timeout)
            if response.status_code == 200 and response.text.strip():
                if (response.text.lower().startswith("<!doctype html>")):
                    continue
                  # Inhalt vorhanden
                if is_htaccess(response.text) or is_wp_config(response.text):
                    preview = textwrap.shorten(response.text, width=50, placeholder="...")
                    logger.info(f"🔴 Sensible Datei gefunden: {file_url} -> {preview}")
                    return True
        
        except requests.exceptions.Timeout:
            logger.info(f"⚠️ Timeout bei {file_url}")
            continue
        except requests.exceptions.ConnectionError:
            logger.info(f"❌ Verbindungsfehler bei {file_url}")
            continue
        except requests.exceptions.RequestException as e:
            logger.info(f"❗ Unbekannter Fehler bei {file_url}: {e}")
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
    logger.info(f"{len(workinglist)} WordPress-Instanzen zu prüfen")
    
    updates = []
    for item in workinglist:
        dns = item.dnsId
        hostname = f"https://{dns.dns}.{dns.tld}"
        result = resolve_directory(hostname, timeout=10) 
        item.open_directory = result
        updates.append(item)

    if updates:
        try:
            Wordpress.objects.bulk_update(updates, ['open_directory'])
        except IntegrityError as e:
            logger.info(f"Fehler beim Aktualisieren der Einträge: {e}")
