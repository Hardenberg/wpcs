import random
import string
import socket
from ..models import TLD

def get_random_length():
    return random.randint(3, 10)

def get_random_strings(length):
    runner = 100
    result = []
    while runner > 0:
        zeichen = string.ascii_lowercase
        result.append(''.join(random.choices(zeichen, k=length)))
        runner -= 1
    return result

def is_valid(item, tld):
    hostname = item + '.' + tld
    try:
        ip_adresse = socket.gethostbyname(hostname)
        return {
            'valid': True,
            'hostname': item,
            'tld': tld,
            'ip': ip_adresse
        }
    except socket.gaierror as e:
        return {
            'valid': False,
            'hostname': "",
            'tld': tld,
            'ip': ""
        }

def execute():
    tlds = TLD.objects.all()
    result = []
    length = get_random_length()
    print('find DNS with len ' + str(length) )
    list = get_random_strings(length)
    for item in list:
        for tld in tlds:
            valid = is_valid(item, tld.tld)
            if not valid['valid']:
                continue
            result.append(valid)
    
    return result    