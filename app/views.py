from django.http import HttpResponse
from django.shortcuts import redirect, render

from .tasks import evaluate_http, find_valid_dns, find_wordpress, wp_php_version, wp_user_enumeration
from . models import *
from django.db.models import Exists, OuterRef, F
from django.db.models import Exists, OuterRef, Subquery
from .tables.wordpress_table import WordpressTable
from .tables.dns_table import DNSTable, DNSFilter
from .tables.crm_tables import CRMTable
from django.contrib import messages
from django_tables2 import SingleTableView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import Wordpress
import asyncio

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

class DNSListView(SingleTableView):
    model = DNS
    table_class = DNSTable
    template_name = "app/dns.html"
    filterset_class = DNSFilter

class WordpressListView(SingleTableView):
    model = Wordpress
    table_class = WordpressTable
    template_name = "app/wordpress.html"

    def get_queryset(self):
         return Wordpress.objects.exclude(version='-') \
        .exclude(version__isnull=True) \
        .annotate(
            has_crm=Exists(CRM.objects.filter(dns=OuterRef('dnsId'))),
            crm_id=Subquery(CRM.objects.filter(dns=OuterRef('dnsId')).values('id')[:1])
        )

class CRMListView(SingleTableView):
    model = CRM
    table_class = CRMTable
    template_name = "app/crm.html"

def crm(request):
    return render(request, 'app/crm.html')

@csrf_exempt 
def add_crm(request):
    print(request.POST)
    if request.method == "POST":
        email = request.POST.get("email")
        dns_id = request.POST.get("dns_id")

        # Hier würdest du das CRM-Objekt speichern oder verarbeiten
        CRM.objects.get_or_create(mail=email, dns_id=dns_id)

        return redirect('wordpress')  # Oder zu einer anderen Seite weiterleiten

    return HttpResponse("Ungültige Anfrage", status=400)

def crm(request, id):
    entry = get_object_or_404(CRM, id=id)  # Holt das Objekt oder gibt 404 zurück
    return render(request, 'app/crm_detail.html', {'entry': entry})

def jobs(request):
    return render(request, 'app/jobs.html')

def jobs_aktionen(request, aktion):
    print(aktion)
    if aktion == 'DNS':
        find_valid_dns()
        ergebnis = "ausgeführt"
        messages.success(request, f"Aktion '{aktion}' erfolgreich ausgeführt: {ergebnis}")
    elif aktion == 'HTTP':
        evaluate_http()
        ergebnis = "ausgeführt"
        messages.success(request, f"Aktion '{aktion}' erfolgreich ausgeführt: {ergebnis}")
    elif aktion == 'WORDPRESS':
        find_wordpress()
        ergebnis = "ausgeführt"
        messages.success(request, f"Aktion '{aktion}' erfolgreich ausgeführt: {ergebnis}")
    elif aktion == 'PHP':
        wp_php_version()
        ergebnis = "ausgeführt"
        messages.success(request, f"Aktion '{aktion}' erfolgreich ausgeführt: {ergebnis}")
    elif aktion == 'USER_ENUM':
        wp_user_enumeration()
        ergebnis = "ausgeführt"
        messages.success(request, f"Aktion '{aktion}' erfolgreich ausgeführt: {ergebnis}")
    else:
        messages.success(request, f"Ungültige Aktion: '{aktion}'")
    return render(request, 'app/jobs.html')