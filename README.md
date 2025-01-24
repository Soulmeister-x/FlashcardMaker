# Flashcard Maker


Ziel des Projekts ist es, aus einem PDF-Vorlesungsskript Fakten zu extrahieren und daraus einfache Fragen und Antworten zu synthetisieren, damit diese als Flashcards in Anki importiert werden können.

## Datenformat

Was sind "die wichtigsten Fakten"?

- Hauptgedanken: Die zentralen Themen oder Argumente des Dokuments.
- Wichtige Daten: Entscheidende Statistiken, Zahlen oder Fakten.
- Schlussfolgerungen: Zusammenfassungen von Erkenntnissen, Vorschlägen oder Empfehlungen.
- Wichtige Zitate: Bemerkenswerte Aussagen oder Zitate von Experten, Forschern oder anderen Mitwirkenden.

### Eingabeformat

Das Format der Eingabedaten ist txt oder pdf.

Um Fragen und Antworten in Anki zu importieren, müssen sie in folgendem Format vorliegen ([Doku](https://docs.ankiweb.net/importing/text-files.html)):
```import.txt
Frage1;Antwort1
Frage2;Antwort2
...
```

- erste Zeile definiert Anzahl der Spalten
- escape characters and newline with quotation marks
- use HTML new lines
