
import tkinter as tk
from tkinter import messagebox
import random
import string

from .engine import HangmanEngine
from .dictionary import WORDS, PHRASES

STOPWORDS = {"A","AN","AND","OR","THE"}

def choose_word() -> str:
    return random.choice(sorted(WORDS)).upper()

def choose_phrase() -> str:
    # 60% curated phrase, otherwise build 2-3 word phrase from dictionary
    if PHRASES and random.random() < 0.6:
        return random.choice(PHRASES).upper()
    # build a random phrase with valid words (avoid tiny stopwords to make it fun)
    pool = [w for w in WORDS if len(w) >= 3 and w.upper() not in STOPWORDS]
    n = random.choice([2,3])
    return " ".join(random.sample(pool, n)).upper()

class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman - TDD UI")
        self.root.geometry("680x480")
        self.root.resizable(False, False)

        # State
        self.engine = None
        self.level_var = tk.StringVar(value="basic")  # 'basic' or 'intermediate'
        self.time_left = 15
        self.timer_job = None

        # ----- Header -----
        title = tk.Label(root, text="Hangman", font=("Segoe UI", 22, "bold"))
        title.pack(pady=6)

        # ----- Controls: Level & New Game -----
        controls = tk.Frame(root)
        controls.pack(pady=4)

        tk.Label(controls, text="Choose level:", font=("Segoe UI", 11)).grid(row=0, column=0, padx=6)
        tk.Radiobutton(controls, text="Basic (Word)", variable=self.level_var, value="basic").grid(row=0, column=1)
        tk.Radiobutton(controls, text="Intermediate (Phrase)", variable=self.level_var, value="intermediate").grid(row=0, column=2)
        tk.Button(controls, text="Start / New Round", command=self.new_round).grid(row=0, column=3, padx=8)
        tk.Button(controls, text="Quit", command=self.root.quit).grid(row=0, column=4, padx=8)

        # ----- Word display -----
        self.word_label = tk.Label(root, text="", font=("Consolas", 30, "bold"))
        self.word_label.pack(pady=12)

        # ----- Info row -----
        info = tk.Frame(root)
        info.pack(pady=4)
        self.lives_label = tk.Label(info, text="Lives: -", font=("Segoe UI", 12))
        self.lives_label.grid(row=0, column=0, padx=10)
        self.wrong_label = tk.Label(info, text="Wrong: -", font=("Segoe UI", 12))
        self.wrong_label.grid(row=0, column=1, padx=10)
        self.timer_label = tk.Label(info, text="Time: 15s", font=("Segoe UI", 12))
        self.timer_label.grid(row=0, column=2, padx=10)

        # ----- Input row -----
        input_row = tk.Frame(root)
        input_row.pack(pady=8)
        tk.Label(input_row, text="Enter a letter:", font=("Segoe UI", 12)).grid(row=0, column=0, padx=6)
        self.entry = tk.Entry(input_row, font=("Segoe UI", 16), width=4, justify="center")
        self.entry.grid(row=0, column=1, padx=6)
        self.entry.bind("<Return>", self.on_guess)
        tk.Button(input_row, text="Guess", command=self.on_guess).grid(row=0, column=2, padx=6)

        # ----- Alphabet buttons -----
        alpha = tk.LabelFrame(root, text="Letters", font=("Segoe UI", 10))
        alpha.pack(pady=10, padx=12, fill="x")
        self.letter_btns = {}
        r = c = 0
        for ch in string.ascii_uppercase:
            b = tk.Button(alpha, text=ch, width=2, command=lambda x=ch: self.guess_letter(x))
            b.grid(row=r, column=c, padx=2, pady=2)
            self.letter_btns[ch] = b
            c += 1
            if c == 13:
                r += 1
                c = 0

        # Hint / status
        self.status_label = tk.Label(root, text="Click 'Start / New Round' to begin.", font=("Segoe UI", 10))
        self.status_label.pack(pady=6)

    # ------------------- Round control -------------------
    def new_round(self):
        # pick answer per level
        level = self.level_var.get()
        answer = choose_word() if level == "basic" else choose_phrase()

        # dictionary validation (tokens must exist)
        from .dictionary import WORDS
        HangmanEngine.validate_answer_with_dictionary(answer, WORDS)

        self.engine = HangmanEngine(answer=answer, max_lives=6)
        self._enable_letters(True)
        self.entry.delete(0, tk.END)
        self.entry.focus_set()
        self.status_label.config(text=f"Level: {level.capitalize()}  |  Guess the answer!")
        self.refresh()
        self.start_timer(15)

    # ------------------- Timer -------------------
    def start_timer(self, seconds=15):
        self.stop_timer()
        self.time_left = seconds
        self._tick()

    def _tick(self):
        self.timer_label.config(text=f"Time: {self.time_left}s")
        if self.engine is None:
            return
        if self.time_left <= 0:
            # apply timeout penalty
            self.engine.timeout_penalty()
            self.refresh()
            if self._check_end():
                return
            self.time_left = 15
        else:
            self.time_left -= 1
        self.timer_job = self.root.after(1000, self._tick)

    def stop_timer(self):
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    # ------------------- Guess flow -------------------
    def on_guess(self, event=None):
        if self.engine is None:
            return
        ch = self.entry.get().strip().upper()
        self.entry.delete(0, tk.END)
        if len(ch) != 1 or not ch.isalpha():
            messagebox.showwarning("Invalid input", "Please enter a single letter (A–Z)." )
            return
        self.guess_letter(ch)

    def guess_letter(self, ch: str):
        if self.engine is None:
            return
        res = self.engine.guess(ch)
        # disable button for that letter
        if ch in self.letter_btns:
            self.letter_btns[ch].config(state=tk.DISABLED)
        # reset timer only on a valid guess (hit/miss/repeat all count as an action)
        self.time_left = 15
        self.refresh()
        self._check_end()

    def _check_end(self) -> bool:
        if self.engine.is_won():
            self.stop_timer()
            self._enable_letters(False)
            messagebox.showinfo("You win!", f"Nice! You guessed: {self.engine.reveal()}" )
            self.status_label.config(text="You won! Start a new round when ready.")
            return True
        if self.engine.is_lost():
            self.stop_timer()
            self._enable_letters(False)
            # reveal full answer
            self.word_label.config(text=" ".join(list(self.engine.reveal())))
            messagebox.showerror("Game Over", f"Out of lives! The answer was: {self.engine.reveal()}" )
            self.status_label.config(text="You lost. Start a new round to try again.")
            return True
        return False

    def _enable_letters(self, enable: bool):
        state = tk.NORMAL if enable else tk.DISABLED
        for b in self.letter_btns.values():
            b.config(state=state)

    # ------------------- UI updates -------------------
    def refresh(self):
        if self.engine is None:
            return
        self.word_label.config(text=self.engine.masked())
        wrong = [w for w in sorted(self.engine.wrong) if w != "TIMEOUT"]
        prefix = "⏰, " if "TIMEOUT" in self.engine.wrong else ""
        wrong_str = prefix + ", ".join(wrong) if (wrong or prefix) else "-"
        self.wrong_label.config(text=f"Wrong: {wrong_str}" )
        self.lives_label.config(text=f"Lives: {self.engine.lives}" )

def main():
    root = tk.Tk()
    app = HangmanApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
