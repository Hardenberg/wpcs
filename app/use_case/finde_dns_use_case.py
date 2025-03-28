import random
import string
import socket
from ..models import TLD
import logging
logger = logging.getLogger('django')

def get_random_length(min_length=3, max_length=7):
    return random.randint(min_length, max_length)

def get_random_strings(length, count=500):
    return [''.join(random.choices(string.ascii_lowercase, k=length)) for _ in range(count)]

def is_valid(item, tld):
    hostname = f"{item}.{tld}"
    
    try:
        ip_address = socket.gethostbyname(hostname)
        return {
            "valid": True,
            "dns": item,
            "tld": tld,
            "ip": ip_address
        }
    except socket.gaierror as e:
        return {
            "valid": False,
            "dns": item,
            "tld": tld,
            "ip": None,
            "error": str(e)  # Fehler als String für Debugging-Zwecke
        }

def execute(minimal = 0):
    result = []
    tlds = TLD.objects.all()

    while True:
        length = get_random_length()
        logger.info('find DNS with len ' + str(length) )
        list = get_random_strings(length)
        for item in list:
            for tld in tlds:
                valid = is_valid(item, tld.tld)
                if not valid['valid']:
                    continue
                result.append(valid)

        logger.info('find DNS with len ' + str(length) + ' done')
        if len(result) >= minimal:
            return result  