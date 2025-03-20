from django.test import TestCase
from ..models import EmailTemplate

class EmailTemplateModelTest(TestCase):
    def test_create_email_template(self):
        template = EmailTemplate.objects.create(
            name="TestTemplate",
            subject="Test Subject",
            body="Hello {{ name }}!"
        )
        self.assertEqual(template.name, "TestTemplate")
        self.assertEqual(template.subject, "Test Subject")
