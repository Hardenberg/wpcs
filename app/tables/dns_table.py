import django_tables2 as tables
from ..models import  DNS
import django_filters as filters      
class DNSTable(tables.Table):
    ip = tables.Column(attrs={"td": {"class": "badge text-bg-primary w-75 h-100 m-1"}})
    class Meta:
        model = DNS
        template_name = "django_tables2/bootstrap5.html"
        fields = ("dns", "tld", "ip", "date")
        


class DNSFilter(filters.FilterSet):
    dns = filters.CharFilter(lookup_expr="icontains", label="DNS-Name")
    tld = filters.CharFilter(lookup_expr="icontains", label="TLD")
    ip = filters.CharFilter(lookup_expr="icontains", label="IP-Adresse")

    class Meta:
        model = DNS
        fields = ["dns", "tld", "ip", "date"]
