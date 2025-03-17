import requests
import re
from ..models import DNS, Wordpress, Http

def execute():
    workingList = Wordpress.objects.filter(php__isnull=True).exclude(version='-')[:100]
    for item in workingList:

        url = 'https://' + item.dnsId.hostname()
        php_versions = [
            get_php_version_via_rest_api(url),
            get_php_version_from_settings(url),
            get_php_version_from_main_page(url),
            get_wordpress_version_readme(url),
        ]
        
        result = result = next((version for version in php_versions if version not in ('-', None)), '-')
        item.php = str(result)
    
    Wordpress.objects.bulk_update(workingList, ['php'])


def get_php_version_via_rest_api(url):
    
    api_url = url.rstrip('/') + '/wp-json'

    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()

        # Prüfe die HTTP-Header auf einen PHP-Hinweis
        powered_by = response.headers.get('X-Powered-By', '')

        if "PHP/" in powered_by:
            return powered_by.split("PHP/")[-1]

    except requests.RequestException as e:
        return '-'

def get_php_version_from_settings(url):
    api_url = url.rstrip('/') + '/wp-json/wp/v2/settings'

    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        return response.json()  # Prüfen, ob die API etwas zur PHP-Version enthält

    except requests.RequestException as e:
        return '-'

def get_php_version_from_main_page(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        server_header = response.headers.get('Server', '')
        powered_by = response.headers.get('X-Powered-By', '')

        php_version = None
        for header in [server_header, powered_by]:
            match = re.search(r'PHP/([\d.]+)', header)
            if match:
                php_version = match.group(1)
                break

        return php_version if php_version else '-'
    
    except requests.RequestException as e:
        return '-'
    
def get_wordpress_version_readme(url):
    readme_url = url.rstrip('/') + '/readme.html'

    try:
        response = requests.get(readme_url, timeout=5)
        response.raise_for_status()
        
        match = re.search(r'WordPress ([\d.]+)', response.text)
        return match.group(1) if match else "-"
    
    except requests.RequestException as e:
        return '-'