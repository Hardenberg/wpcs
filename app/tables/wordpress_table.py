import django_tables2 as tables
from ..models import Wordpress

class WordpressTable(tables.Table):
    version = tables.Column(attrs={"td": {"class": "badge text-bg-primary w-75 h-100 m-1"}})
    class Meta:
        model = Wordpress
        template_name = "django_tables2/bootstrap5.html"
        fields = ("dnsId.hostname", "version", "user_enumeration", "date")