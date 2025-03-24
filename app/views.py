from django.http import HttpResponse
from django.shortcuts import redirect, render

from .tasks import evaluate_http, find_open_directory, find_security_txt, find_valid_dns, find_wordpress, wp_php_version, wp_user_enumeration, wp_xmlrpc, finde_subdomains
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
        'user_enum': user_enum,
        'xml_rpc': Wordpress.objects.filter(xml_rpc = True).count(),
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
    aktionen_map = {
        'DNS': find_valid_dns,
        'HTTP': evaluate_http,
        'WORDPRESS': find_wordpress,
        'PHP': wp_php_version,
        'USER_ENUM': wp_user_enumeration,
        'SECU_TXT': find_security_txt,
        'XML_RPC': wp_xmlrpc,
        'OPEN_DICT': find_open_directory,
        'SUBDOMAINS': finde_subdomains
    }

    if aktion in aktionen_map:
        aktionen_map[aktion]()  # Ruft die Funktion dynamisch auf
        ergebnis = "ausgeführt"
        messages.success(request, f"Aktion '{aktion}' erfolgreich ausgeführt: {ergebnis}")
    else:
        messages.error(request, f"Ungültige Aktion: '{aktion}'")

    return render(request, 'app/jobs.html')


def subdomains_fileUpload(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        selected_tld = request.POST.get("tld", "").strip().lower()

        if not file:
            messages.error(request, "⚠️ Bitte eine Datei auswählen.")
            return render(request, 'app/subdomain_upload.html', {'tlds': TLD.objects.all()})

        if not selected_tld:
            messages.error(request, "⚠️ Bitte eine TLD auswählen.")
            return render(request, 'app/subdomain_upload.html', {'tlds': TLD.objects.all()})

        try:
            tld = TLD.objects.get(tld=selected_tld)
        except TLD.DoesNotExist:
            messages.error(request, f"⚠️ TLD '{selected_tld}' existiert nicht.")
            return render(request, 'app/subdomain_upload.html', {'tlds': TLD.objects.all()})

        if file.name.endswith('.txt'):
            content = file.read().decode('utf-8')
            subdomains = content.split('\n')

            for subdomain in subdomains:
                subdomain = subdomain.strip().lower()
                if subdomain:
                    SubdomainsTop100Liste.objects.get_or_create(sub=subdomain, tld=tld)

            messages.success(request, f"Datei erfolgreich hochgeladen und Subdomains hinzugefügt.")
        else:
            messages.error(request, "⚠️ Bitte eine .txt-Datei hochladen.")
    
    ctx = {
        'tlds': TLD.objects.all()
    }
    return render(request, 'app/subdomain_upload.html', ctx)