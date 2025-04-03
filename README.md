# M165 Family Tree

## Projektauftrag

![Komponentendiagramm](/Komponentendiagramm.png)
*Komponentendiagramm*

Die Family Tree Management-Anwendung bietet eine benutzerfreundliche CLI zur Verwaltung von Familiendaten. Sie ermöglicht das Einfügen von Beispieldaten, das Anzeigen des Stammbaums, die Suche nach Personen sowie das Hinzufügen, Aktualisieren und Löschen von Personen. Auch die Verwaltung von Ehe- und Eltern-Kind-Beziehungen sowie die visuelle Darstellung des Stammbaums sind integriert. Statistische Funktionen wie die Ermittlung der Personen mit den meisten Kindern oder die Gesamtanzahl der Personen ergänzen die Funktionalitäten. Die Anwendung unterstützt effiziente Organisation und Analyse genealogischer Informationen.

![Demodaten](/demoData.png)
*Demodaten*

## Erste Schritte

1. Erstelle eine `.env`-Datei im Projektverzeichnis mit folgendem Inhalt:
```
CONNECTION_STRING_DB="<yourConnectionString>"
USERNAME_DB="<yourUsername>"
PASSWORD_DB="<yourPassword>"`
```
2. Richte eine virtuelle Umgebung ein und installiere die benötigten Abhängigkeiten:
```
pip install dotenv
pip install neo4j
pip install networkx
pip install matplotlib
```
1. Starte das Skript `main.py`:
```
python main.py
```