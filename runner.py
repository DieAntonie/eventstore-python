# tests/runner.py
import unittest

# import your test modules
from src.CafeTests import TabTests
from src.DungeonsDragonsTests import (
    CharacterTests,
    EnvironmentTests,
    GameTests
)

# initialize the test suite
loader = unittest.TestLoader()
runner = unittest.TextTestRunner(verbosity=3)

# add tests to the test suite
print("Running Tab Tests")
runner.run(loader.loadTestsFromModule(TabTests))
print("Running Character Tests")
runner.run(loader.loadTestsFromModule(CharacterTests))
print("Running Environment Tests")
runner.run(loader.loadTestsFromModule(EnvironmentTests))
print("Running Game Tests")
print("- Race Tests")
runner.run(loader.loadTestsFromModule(GameTests.RaceTests))
