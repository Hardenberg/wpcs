from django.shortcuts import render
from . models import *

def app(request):
    return render(request, 'app/app.html')

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
            'version': item.version
            
        })
    print(result[0]['version'])
    ctx = {'result': result}
    return render(request,'app/wordpress.html', ctx)