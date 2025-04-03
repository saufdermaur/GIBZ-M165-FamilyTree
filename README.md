# M165 Family Tree

## Projektauftrag

![Komponentendiagramm](/Komponentendiagramm.png)
*Komponentendiagramm*

Die Family Tree Management-Anwendung bietet eine benutzerfreundliche CLI zur Verwaltung von Familiendaten. Sie ermöglicht das Einfügen von Beispieldaten, das Anzeigen des Stammbaums, die Suche nach Personen sowie das Hinzufügen, Aktualisieren und Löschen von Personen. Auch die Verwaltung von Ehe- und Eltern-Kind-Beziehungen sowie die visuelle Darstellung des Stammbaums sind integriert. Statistische Funktionen wie die Ermittlung der Personen mit den meisten Kindern oder die Gesamtanzahl der Personen ergänzen die Funktionalitäten. Die Anwendung unterstützt effiziente Organisation und Analyse genealogischer Informationen.

![Demodaten](/demoData.png)
*Demodaten*

## Getting started

1. Create a `.env` file in the project directory with the following content:
```
CONNECTION_STRING_DB="<yourConnectionString>"
USERNAME_DB="<yourUsername>"
PASSWORD_DB="<yourPassword>"`
```
2. Set up a virtual environment and install the required dependencies:
```
pip install dotenv
pip install neo4j
pip install networkx
pip install matplotlib
```
3. Run `main.py` to get started:
```
python main.py
```