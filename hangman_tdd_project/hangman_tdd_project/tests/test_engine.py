
import unittest
from hangman.engine import HangmanEngine

class TestHangmanEngine(unittest.TestCase):
    def setUp(self):
        self.engine = HangmanEngine(answer="HELLO WORLD", max_lives=3)

    def test_initial_mask(self):
        masked = self.engine.masked()
        # Should be underscores for letters and spaces preserved
        self.assertIn("_", masked)
        self.assertIn("  ", masked)  # double space for space position

    def test_hit_guess(self):
        res = self.engine.guess('L')
        self.assertEqual(res, "hit")
        self.assertIn('L', self.engine.guessed)
        self.assertEqual(self.engine.lives, 3)

    def test_miss_guess(self):
        res = self.engine.guess('Z')
        self.assertEqual(res, "miss")
        self.assertIn('Z', self.engine.wrong)
        self.assertEqual(self.engine.lives, 2)

    def test_repeat_guess(self):
        self.engine.guess('H')
        res = self.engine.guess('H')
        self.assertEqual(res, "repeat")
        self.assertEqual(self.engine.lives, 3)

    def test_win_condition(self):
        for ch in set("HELLOWRD"):  # all unique letters except ' ' and 'L' included
            self.engine.guess(ch)
        # ensure 'L' guessed too so all letters revealed
        self.engine.guess('L')
        self.assertTrue(self.engine.is_won())
        self.assertTrue(self.engine.is_over())

    def test_lose_condition(self):
        self.engine.guess('X')
        self.engine.guess('Y')
        self.engine.guess('Z')
        self.assertTrue(self.engine.is_lost())
        self.assertTrue(self.engine.is_over())

    def test_timeout_penalty(self):
        before = self.engine.lives
        self.engine.timeout_penalty()
        self.assertEqual(self.engine.lives, before - 1)
        self.assertIn("TIMEOUT", self.engine.wrong)

    def test_invalid_guess(self):
        with self.assertRaises(ValueError):
            self.engine.guess('')  # empty
        with self.assertRaises(ValueError):
            self.engine.guess('ab')  # multi-char
        with self.assertRaises(ValueError):
            self.engine.guess('1')  # non-alpha

if __name__ == "__main__":
    unittest.main(verbosity=2)
