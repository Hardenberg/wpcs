from django.shortcuts import render
from . models import *
from .tables.wordpress_table import WordpressTable
from .tables.dns_table import DNSTable
from django_tables2 import SingleTableView

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

class WordpressListView(SingleTableView):
    model = Wordpress
    table_class = WordpressTable
    template_name = "app/wordpress.html"

    def get_queryset(self):
        return Wordpress.objects.all().exclude(version = '-').exclude(version__isnull=True)