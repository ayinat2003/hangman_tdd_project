
import sys
import pathlib
import unittest

# Ensure project root is on the import path
ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

# Discover and run tests under ./tests
unittest.main(module=None, argv=[
    "ignored", "discover",
    "-s", "tests",
    "-t", ".",
    "-p", "test_*.py",
    "-v",
])
