import random
import string
import socket

TLD = 'de'

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

def is_valid(item):
    hostname = item + '.' + TLD
    try:
        ip_adresse = socket.gethostbyname(hostname)
        return {
            'valid': True,
            'hostname': item,
            'tld': TLD,
            'ip': ip_adresse
        }
    except socket.gaierror as e:
        return {
            'valid': False,
            'hostname': "",
            'tld': TLD,
            'ip': ""
        }

def execute():
    result = []
    length = get_random_length()
    list = get_random_strings(length)
    for item in list:
        valid = is_valid(item)
        if not valid['valid']:
            continue
        result.append(valid)
    
    return result    