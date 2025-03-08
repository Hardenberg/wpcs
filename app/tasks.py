from celery import shared_task
import datetime
from .use_case import finde_dns_use_case, schreibe_dns_use_case, evaluiere_http

@shared_task
def print_zeit():
    now = datetime.datetime.now()
    print(f"Die aktuelle Zeit ist {now}")
    return now

@shared_task
def find_valid_dns():
    list = finde_dns_use_case.execute()
    schreibe_dns_use_case.execute(list)
    return list

def evaluate_http():
    evaluiere_http.execute()