
# Hangman (TDD + UI with 15s timer)

Two levels:
- **Basic**: random *word*.
- **Intermediate**: random *phrase* (two or more valid words).

**Rules**
- Underscores show hidden letters.
- 15-second countdown per guess; timeout deducts one life.
- Wrong guess deducts one life.
- Correct guesses reveal all matching letters.
- Win = all letters revealed. Lose = lives reach 0. On loss, answer is shown.
- Play new rounds until you quit.

## Project layout

```
hangman_tdd_project/
├─ hangman/
│  ├─ __init__.py
│  ├─ dictionary.py      # WORDS + PHRASES and helpers
│  ├─ engine.py          # Pure game logic (unit-tested)
│  └─ ui.py              # Tkinter UI + 15s timer
├─ tests/
│  ├─ test_dictionary.py # Dictionary + validation tests
│  └─ test_engine.py     # Engine behavior tests
├─ main.py               # Entry point (runs UI)
└─ README.md
```

## How to run (Windows / macOS / Linux)

Create and activate a virtual environment (optional but recommended), install nothing (Tkinter ships with Python), then:

```bash
cd hangman_tdd_project
python -m unittest -v
python main.py
```

If `python` maps to Python 2 on your system, replace with `python3`.

## TDD approach (what's tested)

- Masking logic (`_ _ _` with spaces preserved)
- Hit/miss/repeat behavior
- Lives decrement on miss and on timeout
- Win/lose detection
- Dictionary validation for words and phrases

UI is intentionally thin and delegates game rules to the engine to keep tests fast and reliable.
