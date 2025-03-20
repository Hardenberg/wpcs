from django.template import Template, Context
from .models import EmailTemplate
from .services import MailgunService

def render_email(template_name, context):
    try:
        template = EmailTemplate.objects.get(name=template_name)
        subject = template.subject
        body = Template(template.body).render(Context(context))
        return subject, body
    except EmailTemplate.DoesNotExist:
        return None, None

def send_templated_email(to, template_name, context):
    subject, body = render_email(template_name, context)
    if subject and body:
        return MailgunService.send_email(to, subject, body)
    return None
