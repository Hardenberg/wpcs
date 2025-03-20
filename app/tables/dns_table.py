import django_tables2 as tables
from ..models import DNS, Http
import django_filters as filters
import django.utils.html as html

class DNSTable(tables.Table):
    ip = tables.Column(attrs={"td": {"class": "badge text-bg-primary w-75 h-100 m-1"}}, verbose_name="IP-Adresse")
    security_txt = tables.Column(verbose_name="security.txt", empty_values=(), attrs={"td": {"class": "short-column"}})

    def render_security_txt(self, record):
        http = Http.objects.filter(dnsId=record.id).first()
        if http and http.has_security_txt:
            return html.mark_safe(
                f'<a href="{http.security_txt}" target="_blank">'
                f'<i class="fas fa-shield-alt text-primary"></i> security.txt</a>'
            )
        return html.mark_safe('<span class="text-muted">-</span>')

    class Meta:
        model = DNS
        template_name = "django_tables2/bootstrap5.html"
        fields = ("dns", "tld", "ip", "security_txt", "date")
        verbose_name_plural = "DNS Einträge"

class DNSFilter(filters.FilterSet):
    dns = filters.CharFilter(lookup_expr="icontains", label="DNS-Name")
    tld = filters.CharFilter(lookup_expr="icontains", label="Top-Level-Domain (TLD)")
    ip = filters.CharFilter(lookup_expr="icontains", label="IP-Adresse")
    date = filters.DateFromToRangeFilter(label="Datum (von/bis)")

    class Meta:
        model = DNS
        fields = ["dns", "tld", "ip", "date"]