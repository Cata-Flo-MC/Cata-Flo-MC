# Jarvis-ähnlicher KI-Assistent (Demo)

Dieses Projekt ist eine **lokale, textbasierte Demo** für einen KI-Assistenten im Stil von „J.A.R.V.I.S.“ aus Marvel. Die Implementierung ist bewusst schlank gehalten und nutzt nur die Python-Standardbibliothek, damit sie sofort lauffähig ist.

## Features

- Dialog im Terminal (Eingabe per Text)
- Modularer Skill-Mechanismus (leicht erweiterbar)
- Einfache „Memory“-Ablage in einer JSON-Datei
- Beispiel-Skills: Uhrzeit/Datum, Rechnen, Notizen, To-do-Liste

## Voraussetzungen

- Python 3.10+ (getestet ohne externe Abhängigkeiten)

## Starten

```bash
python main.py
```

## Beispiele

```text
> wie spät ist es?
> rechne 12 * 7
> merke dir: bringe das paket um 17 uhr raus
> zeige notizen
> todo hinzufügen: test schreiben
> todo liste
```

## Erweiterung

Neue Skills können in `jarvis/skills.py` ergänzt werden. Jeder Skill implementiert zwei Methoden:

- `matches(text: str) -> bool`
- `run(text: str, memory: MemoryStore) -> str`

Der Assistent lädt alle Skills automatisch und leitet Anfragen an das erste passende Modul weiter.

## Hinweis

Diese Demo ist **kein echter LLM**. Sie ist eine solide Basis, um Sprachmodelle (z. B. via API), Sprach-Ein/Ausgabe und Automationsfunktionen nachzurüsten.
