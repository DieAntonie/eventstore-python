import uuid
from ..Edument_CQRS.BDDTest import BDDTest
from ..DungeonsDragons.Character.CharacterAggregate import CharacterAggregate
from ..DungeonsDragons.Character.CharacterRace import (
    Dragonborn,
    Alignment
)

class CharacterTests(BDDTest):

    def setUp(self):
        self.sut = CharacterAggregate()
        self.testId = uuid.uuid1()
        self.testRace = Dragonborn.Green
        self.testAge = 50
        self.testAlignment = Alignment.Neutral

    def test_can_set_character_race(self):
        self.Test(
            self.Given(),
            self.When(
                SetCharacterRace(
                    self.testId,
                    self.testRace,
                    self.testAge,
                    self.testAlignment
                )
            ),
            self.Then(
                CharacterRaceSet(
                    self.testId,
                    self.testTable,
                    self.testWaiter
                )
            )
        )


if __name__ == '__main__':
    unittest.main()
