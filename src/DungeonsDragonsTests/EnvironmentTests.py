import unittest
import uuid
from ..Edument_CQRS.BDDTest import BDDTest


class EnvironmentTests(unittest.TestCase):

    def setUp(self):
        self.BDDTest = BDDTest(self)


if __name__ == '__main__':
    unittest.main()
