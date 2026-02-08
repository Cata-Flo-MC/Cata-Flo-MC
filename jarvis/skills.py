from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from typing import List, Protocol

from jarvis.memory import MemoryStore


class Skill(Protocol):
    name: str

    def matches(self, text: str) -> bool:
        ...

    def run(self, text: str, memory: MemoryStore) -> str:
        ...


@dataclass
class TimeSkill:
    name: str = "time"

    def matches(self, text: str) -> bool:
        return any(keyword in text for keyword in ["uhrzeit", "zeit", "datum", "tag"])

    def run(self, text: str, memory: MemoryStore) -> str:
        now = dt.datetime.now()
        if "datum" in text or "tag" in text:
            return f"Heute ist {now:%d.%m.%Y}."
        return f"Es ist {now:%H:%M} Uhr."


@dataclass
class MathSkill:
    name: str = "math"

    def matches(self, text: str) -> bool:
        return text.startswith("rechne") or bool(re.search(r"\d", text))

    def run(self, text: str, memory: MemoryStore) -> str:
        expression = text.replace("rechne", "").strip()
        expression = expression.replace("x", "*").replace("×", "*")
        if not expression:
            return "Bitte gib einen Ausdruck an, z. B. 'rechne 12 * 7'."
        if not re.fullmatch(r"[\d\s\.\+\-\*\/\(\)]+", expression):
            return "Ich kann nur einfache Rechenausdrücke mit + - * / verarbeiten."
        try:
            result = eval(expression, {"__builtins__": {}}, {})
        except ZeroDivisionError:
            return "Division durch 0 ist nicht erlaubt."
        except Exception:
            return "Der Ausdruck konnte nicht berechnet werden."
        return f"Das Ergebnis ist {result}."


@dataclass
class NoteSkill:
    name: str = "notes"

    def matches(self, text: str) -> bool:
        return text.startswith("merke") or "notiz" in text

    def run(self, text: str, memory: MemoryStore) -> str:
        if text.startswith("merke"):
            note = text.replace("merke", "").replace("dir", "").strip(" :")
            if not note:
                return "Sag mir, was ich mir merken soll."
            memory.add_note(note)
            return "Notiz gespeichert."
        if "zeige" in text or "liste" in text:
            notes = memory.list_notes()
            if not notes:
                return "Keine Notizen vorhanden."
            formatted = "\n".join(f"- {note}" for note in notes)
            return f"Deine Notizen:\n{formatted}"
        return "Du kannst sagen: 'merke dir: ...' oder 'zeige notizen'."


@dataclass
class TodoSkill:
    name: str = "todo"

    def matches(self, text: str) -> bool:
        return text.startswith("todo") or "aufgabe" in text

    def run(self, text: str, memory: MemoryStore) -> str:
        if "hinzuf" in text or text.startswith("todo hinzufügen"):
            todo = text.replace("todo hinzufügen", "").replace("hinzufügen", "").strip(" :")
            if not todo:
                return "Welche Aufgabe soll ich hinzufügen?"
            memory.add_todo(todo)
            return "Aufgabe zur Liste hinzugefügt."
        if "liste" in text or "zeige" in text:
            todos = memory.list_todos()
            if not todos:
                return "Deine To-do-Liste ist leer."
            formatted = "\n".join(f"- {todo}" for todo in todos)
            return f"To-do-Liste:\n{formatted}"
        return "Du kannst sagen: 'todo hinzufügen: ...' oder 'todo liste'."


@dataclass
class FallbackSkill:
    name: str = "fallback"

    def matches(self, text: str) -> bool:
        return True

    def run(self, text: str, memory: MemoryStore) -> str:
        return (
            "Ich bin mir nicht sicher, wie ich helfen kann. "
            "Versuche z. B. 'wie spät ist es?' oder 'rechne 3 + 4'."
        )


def default_skills() -> List[Skill]:
    return [TimeSkill(), MathSkill(), NoteSkill(), TodoSkill(), FallbackSkill()]
