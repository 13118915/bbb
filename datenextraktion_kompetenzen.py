import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

# Liste der URLs für jedes Fach
subjects_links = [
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/altgriechisch/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/astronomie/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/biologie/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/chemie/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/chinesisch/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/deutsch-bb/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/deutsch-be/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/deutsche-gebaerdensprache/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/englisch/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/ethik/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/franzoesisch/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/geografie/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/geschichte/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/gewi-56/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/hebraeisch/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/informatik/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/italienisch/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/japanisch/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/kunst/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/latein/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/l-e-r/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/mathematik-bb/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/mathematik-be/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/musik/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/nawi-56/naturwissenschaften5-6",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/nawi-7-10/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/neugriechisch/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/philosophie/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/physik/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/politische-bildung/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/polnisch/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/portugiesisch/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/psychologie/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/russisch/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/sachunterricht/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/sorbischwendisch/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/sozialwissenschaften-wirtschaftswissenschaft/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/spanisch/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/sport/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/theater/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/tuerkisch/kompetenzen-und-standards",
"https://bildungsserver.berlin-brandenburg.de/rlp-online/c-faecher/w-a-t/kompetenzen-und-standards"
]

# Standard Header (um als normaler Webbrowser identifiziert zu werden)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

for url in subjects_links:
    fach_name = url.split("/")[-2]  # Der Fachname ist das vorletzte Element der URL
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    data = []

    kompetenzbereiche = soup.find_all('section', class_='rlp-kompetenzbereich')
    for kompetenzbereich in kompetenzbereiche:
        kompetenzbereich_name = kompetenzbereich.find('h2').text.strip() if kompetenzbereich.find('h2') else ""
        
        standards = kompetenzbereich.find_all('div', class_='standardRow')
        for standard in standards:
            niveaustufe = standard.find('b').text.strip() if standard.find('b') else ""
            standard_text_element = standard.find('div', class_='col-sm')
            if standard_text_element:
                standard_text = standard_text_element.find('b').text.strip() if standard_text_element.find('b') else ""
            else:
                standard_text = ""
            
            fähigkeiten = [li.text.strip() for li in standard.find_all('li')]
            for fähigkeit in fähigkeiten:
                if fähigkeit and niveaustufe:
                    data.append([kompetenzbereich_name, niveaustufe, standard_text, fähigkeit])

    df = pd.DataFrame(data, columns=['Kompetenzbereich', 'Niveaustufe', 'Standard', 'Fähigkeiten'])
    # Entferne doppelte Zeilen basierend auf der Spalte 'Fähigkeiten'
    df = df.drop_duplicates(subset='Fähigkeiten')
    
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect(f"{fach_name}.db")
    # Speichern Sie die Daten in eine SQLite-Datenbanktabelle
    df.to_sql('kompetenzen_standards', conn, if_exists='replace', index=False)
    # Schließen Sie die Datenbankverbindung
    conn.close()
