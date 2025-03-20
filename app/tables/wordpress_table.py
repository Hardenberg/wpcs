import django_tables2 as tables
from ..models import Wordpress
from django.utils.safestring import mark_safe

class WordpressTable(tables.Table):
    version = tables.Column(attrs={"td": {"class": "badge text-bg-primary w-75 h-100 m-1"}}, verbose_name="Version")
    CRM = tables.Column(empty_values=(), verbose_name="Aktion")

    def render_CRM(self, value, record):
        if not record.has_crm:
            return mark_safe(f'''
                <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#modal-{record.id}">
                    Add CRM
                </button>

                <div class="modal fade" id="modal-{record.id}" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Aktion für {record.dnsId.hostname()}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>

                            <form id="crmForm-{record.id}" class="crm-form" method="post" action="/create-crm">
                                <div class="modal-body">
                                    <input type="hidden" name="dns_id" value="{record.dnsId.id}">
                                    <div class="input-group mb-3">
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

                <script>
                    document.addEventListener('DOMContentLoaded', function() {{
                        const form = document.getElementById('crmForm-{record.id}');
                        form.addEventListener('submit', function(event) {{
                            event.preventDefault(); // Verhindert das Neuladen der Seite
                            const formData = new FormData(form);

                            fetch('/create-crm', {{
                                method: 'POST',
                                body: formData,
                                headers: {{
                                    'X-CSRFToken': getCookie('csrftoken') // CSRF-Token hinzufügen
                                }}
                            }})
                            .then(response => response.json())
                            .then(data => {{
                                if (data.success) {{
                                    window.location.reload(); // Seite neu laden oder Nachricht anzeigen
                                }} else {{
                                    alert('Fehler beim Ausführen der Aktion.'); // Fehler anzeigen
                                }}
                            }});
                        }});
                    }});

                    function getCookie(name) {{
                        let cookieValue = null;
                        if (document.cookie && document.cookie !== '') {{
                            const cookies = document.cookie.split(';');
                            for (let i = 0; i < cookies.length; i++) {{
                                const cookie = cookies[i].trim();
                                if (cookie.substring(0, name.length + 1) === (name + '=')) {{
                                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                    break;
                                }}
                            }}
                        }}
                        return cookieValue;
                    }}
                </script>
            ''')
        else:
            return mark_safe(f'<a href="/crm/{record.crm_id}" class="btn btn-secondary btn-sm">CRM</a>')

    class Meta:
        model = Wordpress
        template_name = "django_tables2/bootstrap5.html"
        fields = ("dnsId.hostname", "version", "user_enumeration", "php", "date", "CRM")
        verbose_name_plural = "Wordpress Einträge"