from django.shortcuts import render
from . models import *

def app(request):
    return render(request, 'app/app.html')

def dns(request):
    dns = DNS.objects.all()
    ctx = {'dns': dns}
    return render(request, 'app/dns.html', ctx)