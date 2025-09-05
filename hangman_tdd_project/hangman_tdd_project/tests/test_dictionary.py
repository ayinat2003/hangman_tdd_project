
import unittest
from hangman.dictionary import WORDS, PHRASES
from hangman.engine import HangmanEngine

class TestDictionaryValidation(unittest.TestCase):
    def test_words_nonempty(self):
        self.assertGreater(len(WORDS), 0)

    def test_phrases_tokens_in_words(self):
        for phrase in PHRASES:
            tokens = [t for t in phrase.split() if t]
            for tok in tokens:
                self.assertIn(tok.lower(), WORDS)

    def test_validate_answer_ok(self):
        HangmanEngine.validate_answer_with_dictionary("data science", WORDS)

    def test_validate_answer_failure(self):
        with self.assertRaises(ValueError):
            HangmanEngine.validate_answer_with_dictionary("notaword xyzzy", WORDS)

if __name__ == "__main__":
    unittest.main(verbosity=2)
