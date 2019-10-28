import uuid
from ..Edument_CQRS.BDDTest import BDDTest
from ..DungeonsDragons.Environment.EnvironmentAggregate import EnvironmentAggregate


class EnvironmentTests(BDDTest):

    def setUp(self):
        self.sut = EnvironmentAggregate()


if __name__ == '__main__':
    unittest.main()
