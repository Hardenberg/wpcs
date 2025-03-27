
import requests
import re
from ..models import Wordpress
import logging
logger = logging.getLogger('django')
def execute():
    workingList = Wordpress.objects.filter(php__isnull=True).exclude(version='-')[:100]
    logger.info(f'Processing {len(workingList)} items')
    for item in workingList:
        url = f'https://{item.dnsId.hostname()}'
        php_version = get_best_php_version(url)
        if php_version:
            item.php = php_version
    Wordpress.objects.bulk_update(workingList, ['php'])

def get_best_php_version(url):
    methods = [
        get_php_version_via_rest_api,
        get_php_version_from_settings,
        get_php_version_from_main_page,
    ]
    for method in methods:
        version = method(url)
        if version and version != '-':
            return version
    return '-'

def get_php_version_via_rest_api(url):
    try:
        response = requests.get(f'{url.rstrip("/")}/wp-json', timeout=5)
        response.raise_for_status()
        powered_by = response.headers.get('X-Powered-By', '')
        if "PHP/" in powered_by:
            return powered_by.split("PHP/")[-1]
    except requests.RequestException:
        return '-'

def get_php_version_from_settings(url):
    try:
        response = requests.get(f'{url.rstrip("/")}/wp-json/wp/v2/settings', timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get('php_version', '-')
    except (requests.RequestException, ValueError):
        return '-'

def get_php_version_from_main_page(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        headers = [response.headers.get('Server', ''), response.headers.get('X-Powered-By', '')]
        for header in headers:
            match = re.search(r'PHP/([\d.]+)', header)
            if match:
                return match.group(1)
    except requests.RequestException:
        return '-'