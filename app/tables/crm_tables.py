import django_tables2 as tables
from ..models import CRM

class CRMTable(tables.Table):
    # version = tables.Column(attrs={"td": {"class": "badge text-bg-primary w-75 h-100 m-1"}})
    class Meta:
        model = CRM
        template_name = "django_tables2/bootstrap5.html"
        fields = ("dns.hostname", "mail", "vendor")