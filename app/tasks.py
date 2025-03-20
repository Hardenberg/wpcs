from celery import shared_task
import datetime
from .use_case import finde_dns_use_case, schreibe_dns_use_case, evaluiere_http, evaluiere_wordpress, evaluiere_php_on_wordpress, evaluiere_security_txt, php_version_control as app_php_version_control
from .use_case.CVE import enumeration_user


@shared_task
def print_zeit():
    now = datetime.datetime.now()
    print(f"Die aktuelle Zeit ist {now}")
    return now

@shared_task
def find_valid_dns():
    list = finde_dns_use_case.execute()
    print(len(list))
    schreibe_dns_use_case.execute(list)
    return list

@shared_task
def evaluate_http():
    print('evaluate HTTPs')
    evaluiere_http.execute()

@shared_task
def find_wordpress():
    print('find Wordpress')
    evaluiere_wordpress.execute()

@shared_task
def wp_user_enumeration():
    print('User Enumeration')
    enumeration_user.execute()

@shared_task
def wp_php_version():
    print('find WP-PHP')
    evaluiere_php_on_wordpress.execute()

@shared_task
def find_security_txt():
    print('find security.txt')
    evaluiere_security_txt.execute()

@shared_task
def php_version_control():
    print('php_version_control')
    app_php_version_control.execute()
    