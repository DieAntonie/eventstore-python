import uuid
from ...Infrastructure.BDDTest import BDDTest
from ...DungeonsDragons.Game.Race.RaceAggregate import RaceAggregate
from ...DungeonsDragons.Game.Race.Commands import (
    CreateCharacterRace,
    ChangeCharacterRaceName,
    AddCharacterSubrace,
    RemoveCharacterSubrace,
    RenameCharacterSubrace,
    SetCharacterRaceAbilityModifiers
)
from ...DungeonsDragons.Game.Race.Events import (
    CharacterRaceCreated,
    CharacterRaceNameChanged,
    CharacterSubraceAdded,
    CharacterSubraceRemoved,
    CharacterSubraceRenamed,
    CharacterRaceAbilityModifiersSet
)
from ...DungeonsDragons.Game.Race.Exceptions import (
    CharacterRaceAlreadyCreated,
    CharacterRaceDoesNotExist,
    CharacterRaceNameDoesNotDiffer,
    CharacterSubraceNameDoesNotDifferFromBaseRace,
    CharacterSubraceAlreadyExists,
    CharacterSubraceDoesNotExists
)


class RaceTests(BDDTest):

    def setUp(self):
        self.sut = RaceAggregate()
        self.testId = uuid.uuid1()
        self.characterRaceName1 = 'Test Race 1'
        self.characterRaceName2 = 'Test Race 2'
        self.characterSubraceName1 = 'Test Subrace 1'
        self.characterSubraceName2 = 'Test Subrace 2'

    def test_can_create_character_race(self):
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

    def test_cannot_create_character_race_more_than_once(self):
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

    def test_cannot_change_uncreated_character_race_name(self):
        self.Test(
            self.Given(),
            self.When(
                ChangeCharacterRaceName(
                    self.testId,
                    self.characterRaceName1
                )
            ),
            self.ThenFailWith(CharacterRaceDoesNotExist)
        )

    def test_cannot_change_character_race_name_to_current_race_name(self):
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
                    self.characterRaceName1
                )
            ),
            self.ThenFailWith(CharacterRaceNameDoesNotDiffer)
        )

    def test_can_add_character_subrace(self):
        self.Test(
            self.Given(
                CharacterRaceCreated(
                    self.testId,
                    self.characterRaceName1
                )
            ),
            self.When(
                AddCharacterSubrace(
                    self.testId,
                    self.characterSubraceName1
                )
            ),
            self.Then(
                CharacterSubraceAdded(
                    self.testId,
                    self.characterSubraceName1
                )
            )
        )

    def test_cannot_add_character_subrace_to_uncreated_race(self):
        self.Test(
            self.Given(),
            self.When(
                AddCharacterSubrace(
                    self.testId,
                    self.characterSubraceName1
                )
            ),
            self.ThenFailWith(CharacterRaceDoesNotExist)
        )

    def test_can_add_multiple_character_subraces(self):
        self.Test(
            self.Given(
                CharacterRaceCreated(
                    self.testId,
                    self.characterRaceName1
                ),
                CharacterSubraceAdded(
                    self.testId,
                    self.characterSubraceName1
                )
            ),
            self.When(
                AddCharacterSubrace(
                    self.testId,
                    self.characterSubraceName2
                )
            ),
            self.Then(
                CharacterSubraceAdded(
                    self.testId,
                    self.characterSubraceName2
                )
            )
        )

    def test_cannot_add_same_character_subrace_more_than_once(self):
        self.Test(
            self.Given(
                CharacterRaceCreated(
                    self.testId,
                    self.characterRaceName1
                ),
                CharacterSubraceAdded(
                    self.testId,
                    self.characterSubraceName1
                )
            ),
            self.When(
                AddCharacterSubrace(
                    self.testId,
                    self.characterSubraceName1
                )
            ),
            self.ThenFailWith(CharacterSubraceAlreadyExists)
        )

    def test_can_remove_character_subrace(self):
        self.Test(
            self.Given(
                CharacterRaceCreated(
                    self.testId,
                    self.characterRaceName1
                ),
                CharacterSubraceAdded(
                    self.testId,
                    self.characterSubraceName1
                )
            ),
            self.When(
                RemoveCharacterSubrace(
                    self.testId,
                    self.characterSubraceName1
                )
            ),
            self.Then(
                CharacterSubraceRemoved(
                    self.testId,
                    self.characterSubraceName1
                )
            )
        )

    def test_can_add_removed_character_subrace(self):
        self.Test(
            self.Given(
                CharacterRaceCreated(
                    self.testId,
                    self.characterRaceName1
                ),
                CharacterSubraceAdded(
                    self.testId,
                    self.characterSubraceName1
                ),
                CharacterSubraceRemoved(
                    self.testId,
                    self.characterSubraceName1
                )
            ),
            self.When(
                AddCharacterSubrace(
                    self.testId,
                    self.characterSubraceName1
                )
            ),
            self.Then(
                CharacterSubraceAdded(
                    self.testId,
                    self.characterSubraceName1
                )
            )
        )

    def test_cannot_removed_character_subrace_more_than_once(self):
        self.Test(
            self.Given(
                CharacterRaceCreated(
                    self.testId,
                    self.characterRaceName1
                ),
                CharacterSubraceAdded(
                    self.testId,
                    self.characterSubraceName1
                ),
                CharacterSubraceRemoved(
                    self.testId,
                    self.characterSubraceName1
                )
            ),
            self.When(
                RemoveCharacterSubrace(
                    self.testId,
                    self.characterSubraceName1
                )
            ),
            self.ThenFailWith(CharacterSubraceDoesNotExists)
        )

    def test_can_rename_character_subrace(self):
        self.Test(
            self.Given(
                CharacterRaceCreated(
                    self.testId,
                    self.characterRaceName1
                ),
                CharacterSubraceAdded(
                    self.testId,
                    self.characterSubraceName1
                )
            ),
            self.When(
                RenameCharacterSubrace(
                    self.testId,
                    self.characterSubraceName1,
                    self.characterSubraceName2
                )
            ),
            self.Then(
                CharacterSubraceRenamed(
                    self.testId,
                    self.characterSubraceName1,
                    self.characterSubraceName2
                )
            )
        )

    def test_can_rename_character_subrace_more_than_once(self):
        self.Test(
            self.Given(
                CharacterRaceCreated(
                    self.testId,
                    self.characterRaceName1
                ),
                CharacterSubraceAdded(
                    self.testId,
                    self.characterSubraceName1
                ),
                CharacterSubraceRenamed(
                    self.testId,
                    self.characterSubraceName1,
                    self.characterSubraceName2
                )
            ),
            self.When(
                RenameCharacterSubrace(
                    self.testId,
                    self.characterSubraceName2,
                    self.characterSubraceName1
                )
            ),
            self.Then(
                CharacterSubraceRenamed(
                    self.testId,
                    self.characterSubraceName2,
                    self.characterSubraceName1
                )
            )
        )

    def test_cannot_rename_unadded_character_subrace(self):
        self.Test(
            self.Given(
                CharacterRaceCreated(
                    self.testId,
                    self.characterRaceName1
                )
            ),
            self.When(
                RenameCharacterSubrace(
                    self.testId,
                    self.characterSubraceName1,
                    self.characterSubraceName2
                )
            ),
            self.ThenFailWith(CharacterSubraceDoesNotExists)
        )

    def test_can_set_race_ability_modifiers(self):
        self.Test(
            self.Given(
                CharacterRaceCreated(
                    self.testId,
                    self.characterRaceName1
                )
            ),
            self.When(
                SetCharacterRaceAbilityModifiers(
                    self.testId,
                    []
                )
            ),
            self.Then(
                CharacterRaceAbilityModifiersSet(
                    self.testId,
                    []
                )
            )
        )

if __name__ == '__main__':
    unittest.main()
