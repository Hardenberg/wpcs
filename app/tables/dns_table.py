import django_tables2 as tables
from ..models import  DNS
        
class DNSTable(tables.Table):
    ip = tables.Column(attrs={"td": {"class": "badge text-bg-primary w-75 h-100 m-1"}})
    class Meta:
        model = DNS
        template_name = "django_tables2/bootstrap5.html"
        fields = ("dns", "tld", "ip", "date")      