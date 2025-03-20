from unittest.mock import patch
from django.test import TestCase
from ..services import MailgunService

class MailgunServiceTest(TestCase):
    @patch('requests.post')
    def test_send_email(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"message": "Queued"}

        status_code, response = MailgunService.send_email(
            "alrik.schnapke@gmail.com", "Test", "Test"
        )

        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "Queued")
