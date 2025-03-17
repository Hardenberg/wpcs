import datetime
from ..models import PHPVersion
from bs4 import BeautifulSoup
import requests 

def execute():
    print('php_version_control')

    url = "https://versionlog.com/php/"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find_all('table', {'class': 'table'})[1]
        if not table:
            print("Tabelle nicht gefunden.")
            return

        rows = table.find_all('tr')[1:]
        print(f"Anzahl der Zeilen: {len(rows)}")
        for row in rows:
            cols = row.find_all('td')
            print(f"Anzahl der Spalten: {len(cols)}")
            #TODO: Implementierung der Datenbank
            # if len(cols) == 6:
            #     version = cols[0].text.strip()
            #     release_date = datetime.datetime.strptime(cols[2].text.strip(), '%Y-%m-%d').date()
            #     active_support = datetime.datetime.strptime(cols[3].text.strip(), '%Y-%m-%d').date()
            #     security_support = datetime.datetime.strptime(cols[4].text.strip(), '%Y-%m-%d').date()
            #     end_of_life = datetime.datetime.strptime(cols[5].text.strip(), '%Y-%m-%d').date()
            #     print(version, release_date, active_support, security_support, end_of_life)
            #     # PHPVersion.objects.update_or_create(
            #     #     version=version,
            #     #     defaults={
            #     #         'release_date': release_date,
            #     #         'active_support': active_support,
            #     #         'security_support': security_support,
            #     #         'end_of_life': end_of_life,
            #     #     }
            #     # )
        print('PHP versions parsed and saved successfully.')
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Seite: {e}")
    except ValueError as e:
        print(f"Fehler beim Parsen des Datums: {e}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")