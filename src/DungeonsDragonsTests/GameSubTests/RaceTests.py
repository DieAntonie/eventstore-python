import uuid
from ...Infrastructure.BDDTest import BDDTest
from ...DungeonsDragons.Game.GameAggregate import GameAggregate
from ...DungeonsDragons.Game.Race.Commands import (
    CreateCharacterRace,
    ChangeCharacterRaceName
)
from ...DungeonsDragons.Game.Race.Events import (
    CharacterRaceCreated,
    CharacterRaceNameChanged
)
from ...DungeonsDragons.Game.Race.Exceptions import (
    CharacterRaceAlreadyCreated,
    CharacterRaceDoesNotExist
)


class RaceTests(BDDTest):

    def setUp(self):
        self.sut = GameAggregate()
        self.testId = uuid.uuid1()
        self.characterRaceName1 = 'Test Race 1'
        self.characterRaceName2 = 'Test Race 2'

    def test_can_add_character_race(self):
        self.Test(
            self.Given(),
            self.When(
                CreateCharacterRace(
                    self.testId,
                    self.characterRaceName1
                )
            ),
            self.Then(
                CharacterRaceCreated(
                    self.testId,
                    self.characterRaceName1
                )
            )
        )

    def test_cannot_add_same_character_race_more_than_once(self):
        self.Test(
            self.Given(
                CharacterRaceCreated(
                    self.testId,
                    self.characterRaceName1
                )
            ),
            self.When(
                CreateCharacterRace(
                    self.testId,
                    self.characterRaceName1
                )
            ),
            self.ThenFailWith(CharacterRaceAlreadyCreated)
        )

    def test_can_change_character_race_name(self):
        self.Test(
            self.Given(
                CharacterRaceCreated(
                    self.testId,
                    self.characterRaceName1
                )
            ),
            self.When(
                ChangeCharacterRaceName(
                    self.testId,
                    self.characterRaceName1,
                    self.characterRaceName2
                )
            ),
            self.Then(
                CharacterRaceNameChanged(
                    self.testId,
                    self.characterRaceName1,
                    self.characterRaceName2
                )
            )
        )

    def test_can_change_character_race_name_more_than_once(self):
        self.Test(
            self.Given(
                CharacterRaceCreated(
                    self.testId,
                    self.characterRaceName1
                ),
                CharacterRaceNameChanged(
                    self.testId,
                    self.characterRaceName1,
                    self.characterRaceName2
                )
            ),
            self.When(
                ChangeCharacterRaceName(
                    self.testId,
                    self.characterRaceName2,
                    self.characterRaceName1
                )
            ),
            self.Then(
                CharacterRaceNameChanged(
                    self.testId,
                    self.characterRaceName2,
                    self.characterRaceName1
                )
            )
        )

    def test_cannot_change_unadded_character_race_name(self):
        self.Test(
            self.Given(
                CharacterRaceCreated(
                    self.testId,
                    self.characterRaceName1
                )
            ),
            self.When(
                ChangeCharacterRaceName(
                    self.testId,
                    self.characterRaceName2,
                    self.characterRaceName2
                )
            ),
            self.ThenFailWith(CharacterRaceDoesNotExist)
        )

    def test_cannot_change_character_race_name_to_existing_race_name(self):
        self.Test(
            self.Given(
                CharacterRaceCreated(
                    self.testId,
                    self.characterRaceName1
                ),
                CharacterRaceCreated(
                    self.testId,
                    self.characterRaceName2
                ),
            ),
            self.When(
                ChangeCharacterRaceName(
                    self.testId,
                    self.characterRaceName1,
                    self.characterRaceName2
                )
            ),
            self.ThenFailWith(CharacterRaceAlreadyCreated)
        )


if __name__ == '__main__':
    unittest.main()
