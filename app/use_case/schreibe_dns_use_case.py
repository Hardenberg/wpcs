from ..models import DNS
import logging
logger = logging.getLogger('django')

def execute(list):
    logger.info(str(len(list)) + ' zu schreiben')
    for item in list:
        DNS.objects.get_or_create(
           dns=item['dns'],
           tld=item['tld'],
           ip=item['ip']
        )