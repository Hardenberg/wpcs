from django.test import TestCase
from rest_framework.test import APIClient
from ..models import EmailTemplate

class EmailTemplateAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.template = EmailTemplate.objects.create(
            name="TestTemplate",
            subject="Hello",
            body="Test Body"
        )

    def test_list_templates(self):
        response = self.client.get('/mailservice/email_templates/')
        self.assertEqual(response.status_code, 200)
