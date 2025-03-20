from django.contrib import admin, messages
from django.shortcuts import redirect

from .utils import send_templated_email
from .models import EmailTemplate

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'updated_at')
    actions = ['send_test_email']

    def send_test_email(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Bitte wähle genau eine Vorlage für den Test", messages.WARNING)
            return redirect("..")

        template = queryset.first()
        recipient = "alrik.schnapke@gmail.com"  # Hier deine eigene Test-Mail-Adresse eintragen
        context = {"name": "Alrik Schnapke"}  # Dummy-Daten für den Platzhalter

        response = send_templated_email(recipient, template.name, context)
        print(response)
        if response:
            self.message_user(request, f"Test-Mail wurde erfolgreich an {recipient} gesendet!", messages.SUCCESS)
        else:
            self.message_user(request, "Fehler beim Versand der Test-Mail!", messages.ERROR)

    send_test_email.short_description = "Test-Mail mit diesem Template senden"