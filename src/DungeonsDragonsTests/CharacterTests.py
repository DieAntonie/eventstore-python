import uuid
from ..Infrastructure.BDDTest import BDDTest
from ..DungeonsDragons.Character.CharacterAggregate import CharacterAggregate
from ..DungeonsDragons.Character.Commands.SetCharacterRace import SetCharacterRace
from ..DungeonsDragons.Character.Events.CharacterRaceSet import CharacterRaceSet
from ..DungeonsDragons.Character.Exceptions import CharacterRaceAlreadySet
from ..DungeonsDragons.Game.Race import Dragonborn
from ..DungeonsDragons.Game.Alignment import Alignment


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
                    self.testRace,
                    self.testAge,
                    self.testAlignment
                )
            )
        )

    def test_cannot_set_character_race_more_than_once(self):
        self.Test(
            self.Given(
                CharacterRaceSet(
                    self.testId,
                    self.testRace,
                    self.testAge,
                    self.testAlignment
                )
            ),
            self.When(
                SetCharacterRace(
                    self.testId,
                    self.testRace,
                    self.testAge,
                    self.testAlignment
                )
            ),
            self.ThenFailWith(CharacterRaceAlreadySet)
        )


if __name__ == '__main__':
    unittest.main()
