
# Bildungsserver Datenextraktion und Datenbankerstellung

Dieses Repository enthält zwei Skripte zur Extraktion von Bildungsdaten von der Webseite des Bildungsservers Berlin-Brandenburg und zur Speicherung dieser Daten in SQLite-Datenbanken.

## Skripte

### datenextraktion_kompetenzen.py

Dieses Skript extrahiert Informationen zu Fachkompetenzen und speichert sie in einer SQLite-Datenbank. Für jedes Fach wird eine separate Datenbankdatei erstellt.

#### Datenbankstruktur

Jede Datenbank enthält eine Tabelle `kompetenzen_standards`, die folgende Spalten hat:

- `Kompetenzbereich`: Der Bereich, zu dem die Kompetenz gehört.
- `Niveaustufe`: Die Niveaustufe der Kompetenz.
- `Standard`: Der Standard, der die Kompetenz beschreibt.
- `Fähigkeiten`: Die spezifischen Fähigkeiten, die mit der Kompetenz verbunden sind.

### datenextraktion_themen.py

Das zweite Skript `datenextraktion_themen.py` navigiert durch die Themen und Inhalte der verschiedenen Fächer und speichert die extrahierten Daten in strukturierten Tabellen innerhalb einer SQLite-Datenbank pro Fach.

#### Datenbankstruktur

Jede Datenbank, die von diesem Skript erstellt wird, enthält mehrere Tabellen:

- `Themenfelder`: Enthält die allgemeinen Themenfelder mit einer eindeutigen ID.
- Weitere Tabellen für jedes Themenfeld: Jede dieser Tabellen enthält Zeilen mit spezifischen Inhalten, die zu dem jeweiligen Themenfeld gehören.

## Anforderungen

- Python 3
- requests
- beautifulsoup4
- pandas (nur für `datenextraktion_kompetenzen.py`)
- sqlite3
- re
- logging

## Installation

Stellen Sie sicher, dass Sie Python 3 und die benötigten Bibliotheken installiert haben. Die Bibliotheken können mit pip installiert werden:

```bash
pip install requests beautifulsoup4 pandas sqlite3
```

## Anwendung

Klonen Sie das Repository und führen Sie die Skripte wie folgt aus:

```bash
git clone https://github.com/IhrBenutzername/Bildungsserver-Datenextraktion.git
cd Bildungsserver-Datenextraktion
python3 datenextraktion_kompetenzen.py
python3 datenextraktion_themen.py
```

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz veröffentlicht. Weitere Informationen finden Sie in der `LICENSE` Datei.

## Kontakt

Bei Fragen oder Unterstützung eröffnen Sie bitte ein Issue oder kontaktieren Sie mich unter mario.scholz@lk.brandenburg.de.
