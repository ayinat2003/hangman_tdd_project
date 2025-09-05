
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Set, Iterable

ALPHABET = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

def _normalize_answer(ans: str) -> str:
    # Uppercase and keep letters/spaces only; collapse multiple spaces
    filtered = []
    prev_space = False
    for ch in ans.upper():
        if ch.isalpha():
            filtered.append(ch)
            prev_space = False
        elif ch.isspace():
            if not prev_space:
                filtered.append(" ")
            prev_space = True
        # ignore punctuation/hyphens for simplicity (could be extended)
    return "".join(filtered).strip()

@dataclass
class HangmanEngine:
    answer: str
    max_lives: int = 6
    guessed: Set[str] = field(default_factory=set)
    wrong: Set[str] = field(default_factory=set)
    lives: int = field(init=False)

    def __post_init__(self):
        self.answer = _normalize_answer(self.answer)
        self.lives = self.max_lives
        # Validate answer isn't empty and contains at least one letter
        if not any(c.isalpha() for c in self.answer):
            raise ValueError("Answer must contain at least one letter.")

    # ----------------- Dictionary validation -----------------
    @staticmethod
    def validate_answer_with_dictionary(answer: str, words: Iterable[str]) -> None:
        """Raise ValueError if any token is not in the provided dictionary set."""
        # tokens are lower-case words; ignore extra spaces
        tokens = [t for t in answer.lower().split() if t]
        missing = [t for t in tokens if t not in set(words)]
        if missing:
            raise ValueError(f"Invalid tokens (not in dictionary): {', '.join(missing)}")


    # ----------------- Game mechanics -----------------
    def unique_letters(self) -> Set[str]:
        return {c for c in self.answer if c.isalpha()}

    def masked(self) -> str:
        # Reveal guessed letters; keep spaces; mask letters with underscores
        parts = []
        for ch in self.answer:
            if ch == " ":
                parts.append("  ")  # two spaces for readability
            elif ch in self.guessed:
                parts.append(ch)
            else:
                parts.append("_")
        # Join with spaces so it looks like "A _ _ E"
        return " ".join(parts)

    def guess(self, ch: str) -> str:
        if not ch or len(ch) != 1 or not ch.isalpha():
            raise ValueError("Guess must be a single A-Z letter.")
        ch = ch.upper()
        if ch in self.guessed or ch in self.wrong:
            return "repeat"
        if ch in self.unique_letters():
            self.guessed.add(ch)
            return "hit"
        else:
            self.wrong.add(ch)
            self.lives -= 1
            return "miss"

    def timeout_penalty(self) -> None:
        """Apply a life penalty due to timer expiry."""
        if self.lives > 0:
            self.lives -= 1
            # Represent timeout as a special entry in wrong set
            self.wrong.add("TIMEOUT") 

    def is_won(self) -> bool:
        return self.unique_letters().issubset(self.guessed)

    def is_lost(self) -> bool:
        return self.lives <= 0

    def is_over(self) -> bool:
        return self.is_won() or self.is_lost()

    def reveal(self) -> str:
        return self.answer
