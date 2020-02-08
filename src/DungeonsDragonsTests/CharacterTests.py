import uuid
from ..Infrastructure.BDDTest import BDDTest
from ..DungeonsDragons.Character.CharacterAggregate import CharacterAggregate
from ..DungeonsDragons.Character.Commands.SetRace import SetRace
from ..DungeonsDragons.Character.Events.RaceSet import RaceSet
from ..DungeonsDragons.Character.Exceptions import RaceAlreadySet
from ..DungeonsDragons.Game.Race.Race import Dragonborn
from ..DungeonsDragons.Game.Alignment import Alignment


class CharacterTests(BDDTest):

    def setUp(self):
        self.sut = CharacterAggregate()
        self.testId = uuid.uuid1()
        self.testRace = Dragonborn.Green
        self.testAge = 50
        self.testAlignment = Alignment.Neutral

    def test_can_set_race(self):
        self.Test(
            self.Given(),
            self.When(
                SetRace(
                    self.testId,
                    self.testRace,
                    self.testAge,
                    self.testAlignment
                )
            ),
            self.Then(
                RaceSet(
                    self.testId,
                    self.testRace,
                    self.testAge,
                    self.testAlignment
                )
            )
        )

    def test_cannot_set_race_more_than_once(self):
        self.Test(
            self.Given(
                RaceSet(
                    self.testId,
                    self.testRace,
                    self.testAge,
                    self.testAlignment
                )
            ),
            self.When(
                SetRace(
                    self.testId,
                    self.testRace,
                    self.testAge,
                    self.testAlignment
                )
            ),
            self.ThenFailWith(RaceAlreadySet)
        )


if __name__ == '__main__':
    unittest.main()
