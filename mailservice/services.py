import requests
from django.conf import settings
import logging
logger = logging.getLogger('django')

class MailgunService:
    @staticmethod
    def send_email(to, subject, body):
        try:
            response = requests.post(
                f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages",
                auth=("api", settings.MAILGUN_API_KEY),
                data={"from": f"Mailgun Sandbox <postmaster@{settings.MAILGUN_DOMAIN}.mailgun.org>",
			"to": "Alrik Schnapke <alrik.schnapke@gmail.com>",
  			"subject": "Hello Alrik Schnapke",
  			"text": "Congratulations Alrik Schnapke, you just sent an email with Mailgun! You are truly awesome!"})
            
            logger.info(settings.MAILGUN_DOMAIN)
            status_code = response.status_code

            if status_code == 200:
                try:
                    return status_code, response.json()
                except requests.exceptions.JSONDecodeError:
                    logger.error("Failed to decode JSON response from Mailgun.")
                    logger.error(f"Mailgun Response Content: {response.content}")
                    return status_code, {"error": "Failed to decode JSON"}
            else:
                logger.error(f"Mailgun API request failed with status code: {status_code}")
                logger.error(f"Mailgun Response Content: {response.content}")
                return status_code, {"error": "Mailgun API request failed"}

        except requests.exceptions.RequestException as e:
            logger.error(f"Mailgun API request exception: {e}")
            return None, {"error": "Mailgun API request exception"}
        except AttributeError:
            logger.error("Mailgun settings not properly configured.")
            return None, {"error": "Mailgun settings not properly configured."}