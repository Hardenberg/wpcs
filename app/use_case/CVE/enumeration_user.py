from ...models import DNS, Http, Wordpress
import requests

def enumeration_users_rest_api(url):
    api_url = url.rstrip('/') + '/wp-json/wp/v2/users'

    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        users = response.json()

        return True if users else False
    
    except requests.RequestException as e:
        return False

def execute():
    wps = Wordpress.objects.filter(user_enumeration=None).exclude(version='-')[:20]
    runner = 0
    for item in wps: 
        dns = DNS.objects.filter(id=item.dnsId_id).first()
        hostname = 'https://'+dns.dns + '.'+dns.tld
        result = enumeration_users_rest_api(hostname)
        item.user_enumeration = result
        item.save()
        if result:
            runner = runner + 1
    print(str(runner) + ' UserEnumeration gefunden')