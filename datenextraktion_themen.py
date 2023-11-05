import requests
from bs4 import BeautifulSoup
import sqlite3
import re
import logging

# Logging-Einstellungen
logging.basicConfig(filename='extraktion.log', level=logging.INFO)

# Liste der URLs für die verschiedenen Fächer
# (Ich habe hier nur ein paar URLs als Beispiel aufgenommen. Sie können die Liste erweitern.)
URLS = [
    "https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/altgriechisch/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/astronomie/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/biologie/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/chemie/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/chinesisch/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/deutsch-bb/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/deutsch-be/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/deutsche-gebaerdensprache/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/englisch/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/ethik/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/franzoesisch/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/geografie/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/geschichte/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/gewi-56/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/hebraeisch/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/informatik/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/italienisch/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/japanisch/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/kunst/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/latein/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/l-e-r/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/mathematik-bb/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/mathematik-be/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/musik/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/nawi-56/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/nawi-7-10/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/neugriechisch/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/philosophie/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/physik/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/politische-bildung/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/polnisch/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/portugiesisch/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/psychologie/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/russisch/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/sachunterricht/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/sorbischwendisch/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/sozialwissenschaften-wirtschaftswissenschaft/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/spanisch/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/sport/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/theater/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/tuerkisch/themen-und-inhalte",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/w-a-t/themen-und-inhalte"
]

def clean_table_name(name):
    sanitized_name = re.sub(r'\W+', '_', name)
    if sanitized_name and sanitized_name[0].isdigit():
        sanitized_name = '_' + sanitized_name
    return sanitized_name

def extract_data_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    themenfelder = [btn.text.strip() for btn in soup.select('.accordion-header button')]
    all_content = []

    for accordion in soup.select('.accordion'):
        content = {}
        for table in accordion.select('table.contenttable'):
            headers = [th.text.strip() for th in table.select('th')]
            if not headers:
                headers = [td.text.strip() for td in table.select('tr')[0].select('td')]
                rows = table.select('tr')[1:]
            else:
                rows = table.select('tr')[1:]
            for row in rows:
                for header, td in zip(headers, row.select('td')):
                    if header not in content:
                        content[header] = []
                    if td.select('li'):
                        content[header].extend([item.text.strip() for item in td.select('li')])
                    else:
                        content[header].append(td.text.strip())

        all_content.append(content)

    return themenfelder, all_content

def save_to_db(themenfelder, all_content, subject_name):
    db_name = f"{subject_name}.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Themenfelder (
        ID INTEGER PRIMARY KEY,
        name TEXT,
        numbers TEXT
    )
    """)

    for themenfeld, content in zip(themenfelder, all_content):
        name = re.sub(r'\d+\.\d+', '', themenfeld).strip()
        match = re.search(r'\d+\.\d+', themenfeld)
        numbers = match.group() if match else '-'
        cursor.execute("INSERT INTO Themenfelder (name, numbers) VALUES (?, ?)", (name, numbers))
        thema_id = cursor.lastrowid

        for table_name, rows in content.items():
            sanitized_table_name = clean_table_name(table_name)
            cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS [{sanitized_table_name}] (
                ID INTEGER PRIMARY KEY,
                ThemaID INTEGER,
                zeile INTEGER,
                name TEXT
            )
            """)
            for idx, row in enumerate(rows, start=1):
                cursor.execute(f"INSERT INTO [{sanitized_table_name}] (ThemaID, zeile, name) VALUES (?, ?, ?)", (thema_id, idx, row))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    for url in URLS:
        subject_name = url.split('/')[-2]  # Nimmt den Namen des vorletzten Verzeichnisses
        logging.info(f"Starte Extraktion für {subject_name}")
        themenfelder, all_content = extract_data_from_url(url)
        save_to_db(themenfelder, all_content, subject_name)
        logging.info(f"Extraktion für {subject_name} abgeschlossen")
