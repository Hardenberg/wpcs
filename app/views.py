from django.shortcuts import render
from . models import *

def app(request):
    dns = DNS.objects.count()
    https = Http.objects.filter(https = True).count()
    wordpress = Wordpress.objects.all().exclude(version = '-').count()
    user_enum = Wordpress.objects.filter(user_enumeration = True).count()
    ctx = {
        'valid_dns': dns,
        'https': https,
        'wordpress': wordpress,
        'user_enum': user_enum
    }
    return render(request, 'app/app.html', ctx)

def dns(request):
    result = []
    dns = DNS.objects.all()[:200]
    for item in dns:
        try:
            http = Http.objects.get(dnsId_id=item.id)
        except:
            http = {}

        item.http = http
        result.append(item)
    ctx = {'dns': result}
    print(dns[0].http.__dict__.keys())
    return render(request, 'app/dns.html', ctx)


def wordpress(request):
    result = []
    wp = Wordpress.objects.all()
    for item in wp:
        try:
            dns = DNS.objects.get(id=item.dnsId_id)
        except:
            continue
        if item.version == '-':
            continue
        result.append({
            'uri': dns.dns + '.' + dns.tld,
            'uri_complete': 'https://'+dns.dns + '.' + dns.tld,
            'version': item.version,
            'user_enumeration':item.user_enumeration
            
        })
    print(result[0]['version'])
    ctx = {'result': result}
    return render(request,'app/wordpress.html', ctx)