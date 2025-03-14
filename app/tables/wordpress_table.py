import django_tables2 as tables
from ..models import Wordpress
from django.utils.safestring import mark_safe

class WordpressTable(tables.Table):
    version = tables.Column(attrs={"td": {"class": "badge text-bg-primary w-75 h-100 m-1"}})
    CRM = tables.Column(empty_values=(), verbose_name="Aktion")

    def render_CRM(self, value, record):
        print(record.has_crm)
        if not record.has_crm:
            return mark_safe(f'''
                <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#modal-{record.id}">
                    Add CRM
                </button>

                <!-- Modal -->
                 <div class="modal fade" id="modal-{ record.id }" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Aktion für { record.dnsId.hostname() }</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>

                            <!-- Formular -->
                            <form id="crmForm-{record.id}" class="crm-form" method="post" action="/create-crm">

                                <div class="modal-body">
                                    <input type="hidden" name="dns_id" value="{ record.dnsId.id }">
                                    <div class="input-group">
                                        <span class="input-group-text">Mail</span>
                                        <input type="email" class="form-control" name="email" placeholder="Mail eingeben" required>
                                    </div>
                                </div>

                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Schließen</button>
                                    <button type="submit" class="btn btn-primary">Aktion ausführen</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            ''')
        else:
            return mark_safe(f'''<a href="/" class="btn btn-secondary btn-sm">CRM</a>''')

    class Meta:
        model = Wordpress
        template_name = "django_tables2/bootstrap5.html"
        fields = ("dnsId.hostname", "version", "user_enumeration", "php", "date", "CRM")

    