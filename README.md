# Projekt W.O.L.F
Projekt W.O.L.F - Wege mit OpenStreetMap Lage Finder
Projekt W.O.L.F - Ways with OpenStreetMap Location Finder
![wolf](gfx/wolf_logo.jpeg)

## Projekt Anforderungen / Ziele
Entwicklung einer grafischen Oberfläche zur Visualisierung von Pfadfindungsalgorithmen.

- Möglichkeit eine beliebige OSM zu laden und das Straßennetz zu extrahieren. (Ob man dies über die webapi geschieht oder über eine heruntergeladene karte wäre mir egal.)
- Unterschiedliche Darstellungsmöglichkeiten der Karte
- Erzeugung des Graphen
- Auswahl zwischen unterschiedlichen Algorithmen zum durchlaufen
- Auswahl des Start und Zielknotens auf der Karte durch klicken (Erweiterbar auf mehrere Ziele, s.d. auch Routen erzeugt werden können)
- Dijkstra, A*, Greedy, (optional Potentialfeldmethode, Routenplanung) 
- Visualisierung des Suchalgorithmus (Einzelne Schritte sukzessive darstellbar)
- Mögliche Programmiersprachen Python, C++, Java
- Cross Plattform Kompatibilität (Windows, MacOS, Linux)

## Anleitung
### 1. Virtenv erstellen
``` bash
python -m venv venv
```
### 2. Virtenv aktivieren

#### Unter Linux:
``` bash
source venv/bin/activate
```

#### Windows:
``` ps
venv/Scripts/Activate.ps1
```
oder
``` bat
venv/Scripts/Activate.bat
```
PS Sktripte könnten deaktivert sein:
``` ps
Get-ExecutionPolicy
```
Als Admin:
``` ps
Set-ExecutionPolicy Unrestricted
```

### 3. Abhänigkeiten installieren
``` bash
pip install -r requirements.txt
```
oder
``` bash
python -m pip install -r requirements.txt
```

### 4. zum venv verlassen

``` bash
deactivate
```
### 5. Programm starten
Im aktiven Virtenv
```
python main.py
```



## Theme umstellen
### main.py
    apply_stylesheet(app, theme='light_amber.xml')

### Mögliche Themes
 'dark_amber.xml',
 'dark_blue.xml',
 'dark_cyan.xml',
 'dark_lightgreen.xml',
 'dark_pink.xml',
 'dark_purple.xml',
 'dark_red.xml',
 'dark_teal.xml',
 'dark_yellow.xml',
 'light_amber.xml',
 'light_blue.xml',
 'light_cyan.xml',
 'light_cyan_500.xml',
 'light_lightgreen.xml',
 'light_pink.xml',
 'light_purple.xml',
 'light_red.xml',
 'light_teal.xml',
 'light_yellow.xml'