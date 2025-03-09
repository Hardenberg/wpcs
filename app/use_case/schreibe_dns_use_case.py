from ..models import DNS

def execute(list):
    print(str(len(list)) + ' zu schreiben')
    for item in list:
        DNS.objects.get_or_create(
           dns=item['hostname'],
           tld=item['tld'],
           ip=item['ip']
        )