from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class MemoryStore:
    path: Path = field(default_factory=lambda: Path("memory.json"))
    data: Dict[str, Any] = field(default_factory=dict)

    def load(self) -> None:
        if self.path.exists():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
        else:
            self.data = {"notes": [], "todos": []}

    def save(self) -> None:
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")

    def add_note(self, note: str) -> None:
        notes: List[str] = self.data.setdefault("notes", [])
        notes.append(note)
        self.save()

    def list_notes(self) -> List[str]:
        return list(self.data.get("notes", []))

    def add_todo(self, todo: str) -> None:
        todos: List[str] = self.data.setdefault("todos", [])
        todos.append(todo)
        self.save()

    def list_todos(self) -> List[str]:
        return list(self.data.get("todos", []))
