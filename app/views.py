from django.http import HttpResponse
from django.shortcuts import redirect, render
from . models import *
from django.db.models import Exists, OuterRef, F
from .tables.wordpress_table import WordpressTable
from .tables.dns_table import DNSTable, DNSFilter
from .tables.crm_tables import CRMTable
from django_tables2 import SingleTableView
from django.views.decorators.csrf import csrf_exempt

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
            has_crm=Exists(CRM.objects.filter(dns=OuterRef('dnsId')))
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