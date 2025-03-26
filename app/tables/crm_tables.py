import django_tables2 as tables
from ..models import CRM
from django.utils.safestring import mark_safe

class CRMTable(tables.Table):
    customer_link = tables.Column(accessor="id", verbose_name="Kundenlink")

    def render_customer_link(self, value):
        
        return mark_safe(f'''<a href="/crm/{value}"class="btn btn-primary btn-sm">Link</a>''')


    class Meta:
        model = CRM
        template_name = "django_tables2/bootstrap5.html"
        fields = ("dns.hostname", "mail", "vendor", "customer_link")