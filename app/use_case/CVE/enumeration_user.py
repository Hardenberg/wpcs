from concurrent.futures import ThreadPoolExecutor, as_completed
from ...models import DNS, Http, Wordpress
import requests

def enumeration_users_rest_api(url):
    api_url = url.rstrip('/') + '/wp-json/wp/v2/users'

    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()

        return bool(response.json())
    
    except requests.RequestException as e:
        return False

def process_wordpress_instance(item):
    dns = DNS.objects.filter(id=item.dnsId_id).first()
    if not dns:
        return item, None 

    hostname = f"https://{dns.dns}.{dns.tld}"
    result = enumeration_users_rest_api(hostname)
    return item, result

def execute():
    wps = Wordpress.objects.filter(user_enumeration=None).exclude(version='-')
    print(f"{len(wps)} WordPress-Instanzen zu prüfen")
    runner = 0
    with ThreadPoolExecutor(max_workers=1) as executor:  # 10 gleichzeitige Threads
        future_to_item = {executor.submit(process_wordpress_instance, item): item for item in wps}

        for future in as_completed(future_to_item):
            item, result = future.result()
            if result is None:
                continue  

            if item.user_enumeration != result: # Nur speichern, wenn sich der Wert geändert hat
                item.user_enumeration = result
                item.save()

            if result:
                runner += 1

    print(f"{runner} UserEnumeration gefunden")