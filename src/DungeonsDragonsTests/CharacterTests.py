import uuid
from ..Edument_CQRS.BDDTest import BDDTest
from ..DungeonsDragons.Character.CharacterAggregate import CharacterAggregate

class CharacterTests(BDDTest):

    def setUp(self):
        self.sut = CharacterAggregate()


if __name__ == '__main__':
    unittest.main()
