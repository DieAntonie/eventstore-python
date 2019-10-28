# tests/runner.py
import unittest

# import your test modules
from src.CafeTests import TabTests
from src.DungeonsDragonsTests import (
    CharacterTests,
    EnvironmentTests
)

# initialize the test suite
loader = unittest.TestLoader()
suite = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(TabTests))
suite.addTests(loader.loadTestsFromModule(CharacterTests))
suite.addTests(loader.loadTestsFromModule(EnvironmentTests))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
