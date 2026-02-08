from __future__ import annotations

from jarvis.memory import MemoryStore
from jarvis.skills import default_skills


class JarvisAssistant:
    def __init__(self) -> None:
        self.memory = MemoryStore()
        self.memory.load()
        self.skills = default_skills()

    def run(self) -> None:
        print("Jarvis-Demo gestartet. Tippe 'exit' zum Beenden.")
        while True:
            try:
                text = input("> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\nBis bald!")
                break
            if text in {"exit", "quit", "ende"}:
                print("Bis bald!")
                break
            if not text:
                continue
            response = self.handle(text)
            print(response)

    def handle(self, text: str) -> str:
        for skill in self.skills:
            if skill.matches(text):
                return skill.run(text, self.memory)
        return "Ich habe gerade keinen passenden Skill."
