from celery import shared_task
import datetime
import time
import logging
from functools import wraps
from .use_case import finde_dns_use_case, schreibe_dns_use_case, evaluiere_http, evaluiere_wordpress, evaluiere_php_on_wordpress, evaluiere_security_txt, php_version_control as app_php_version_control, finde_subdomains as subdomains_use_case
from .use_case.CVE import enumeration_user, wp_xmlrpc as wp_xmlrpc_use_case, open_directory

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,  # Log-Level (z.B. INFO, DEBUG, etc.)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def measure_runtime(func):
    """
    Decorator, der die Laufzeit einer Funktion misst und protokolliert.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        runtime = end_time - start_time
        logger.info(f"Die Funktion '{func.__name__}' hat {runtime:.6f} Sekunden benötigt.")
        return result
    return wrapper

@shared_task
@measure_runtime
def print_zeit():
    now = datetime.datetime.now()
    print(f"Die aktuelle Zeit ist {now}")
    return now

@shared_task
@measure_runtime
def find_valid_dns(minimal = 0):
    list = finde_dns_use_case.execute(minimal)
    print(len(list))
    schreibe_dns_use_case.execute(list)
    return list

@shared_task
@measure_runtime
def evaluate_http():
    print('evaluate HTTPs')
    evaluiere_http.execute()

@shared_task
@measure_runtime
def find_wordpress():
    print('find Wordpress')
    evaluiere_wordpress.execute()

@shared_task
@measure_runtime
def wp_user_enumeration():
    print('User Enumeration')
    enumeration_user.execute()

@shared_task
@measure_runtime
def wp_php_version():
    print('find WP-PHP')
    evaluiere_php_on_wordpress.execute()

@shared_task
@measure_runtime
def find_security_txt():
    print('find security.txt')
    evaluiere_security_txt.execute()

@shared_task
@measure_runtime
def php_version_control():
    print('php_version_control')
    app_php_version_control.execute()

@shared_task
@measure_runtime
def wp_xmlrpc():
    print('wp_xmlrpc')
    wp_xmlrpc_use_case.execute()

@shared_task
@measure_runtime
def find_open_directory():
    print('open_directory')
    open_directory.execute()

@shared_task
@measure_runtime
def finde_subdomains():
    logger.info('subdomains')
    subdomains_use_case.execute()
    
@shared_task
@measure_runtime
def complete():
    # print_zeit()
    find_valid_dns(100)
    evaluate_http()
    find_wordpress()
    wp_user_enumeration()
    wp_php_version()
    # find_security_txt()
    # php_version_control()
    wp_xmlrpc()
    find_open_directory()
    # finde_subdomains()
    logger.info('Complete')