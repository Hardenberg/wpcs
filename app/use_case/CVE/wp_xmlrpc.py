from concurrent.futures import ThreadPoolExecutor
import requests
import logging
from ...models import Wordpress
import logging
logger = logging.getLogger('django')

logger = logging.getLogger(__name__)

def check_xmlrpc(url):
    xmlrpc_url = url.rstrip('/') + '/xmlrpc.php'
    
    try:
        response = requests.post(
            xmlrpc_url,
            data="<methodCall><methodName>system.listMethods</methodName></methodCall>",
            headers={'Content-Type': 'text/xml'},
            timeout=5
        )

        if response.status_code == 200 and "methodResponse" in response.text:
            return 1
        return 0
    
    except requests.RequestException as e:
        logger.warning(f"XML-RPC check failed for {xmlrpc_url}: {e}")
        return 0

def process_item(item):
    dns = item.dnsId
    hostname = f"https://{dns.dns}.{dns.tld}"
    item.xml_rpc = check_xmlrpc(hostname)
    return item

def execute():
    workinglist = Wordpress.objects.filter(xml_rpc=None).exclude(version='-').select_related('dnsId')
    logger.info(f"{len(workinglist)} WordPress-Instanzen zu prüfen")
    with ThreadPoolExecutor(max_workers=1) as executor:
        results = list(executor.map(process_item, workinglist))

    if results:
        Wordpress.objects.bulk_update(results, ['xml_rpc'])