import uuid
from ...Infrastructure.BDDTest import BDDTest
from ...DungeonsDragons.Game.Race.RaceAggregate import RaceAggregate
from ...DungeonsDragons.Game.Race.Commands import (
    CreateRace,
    ChangeRaceName,
    Addsubrace,
    Removesubrace,
    Renamesubrace,
    SetRaceAbilityModifiers
)
from ...DungeonsDragons.Game.Race.Events import (
    RaceCreated,
    RaceNameChanged,
    subraceAdded,
    subraceRemoved,
    subraceRenamed,
    RaceAbilityModifiersSet
)
from ...DungeonsDragons.Game.Race.Exceptions import (
    RaceAlreadyCreated,
    RaceDoesNotExist,
    RaceNameDoesNotDiffer,
    subraceNameDoesNotDifferFromBaseRace,
    subraceAlreadyExists,
    subraceDoesNotExists
)


class RaceTests(BDDTest):

    def setUp(self):
        self.sut = RaceAggregate()
        self.testId = uuid.uuid1()
        self.RaceName1 = 'Test Race 1'
        self.RaceName2 = 'Test Race 2'
        self.subraceName1 = 'Test Subrace 1'
        self.subraceName2 = 'Test Subrace 2'

    def test_can_create_race(self):
        self.Test(
            self.Given(),
            self.When(
                CreateRace(
                    self.testId,
                    self.RaceName1
                )
            ),
            self.Then(
                RaceCreated(
                    self.testId,
                    self.RaceName1
                )
            )
        )

    def test_cannot_create_race_more_than_once(self):
        self.Test(
            self.Given(
                RaceCreated(
                    self.testId,
                    self.RaceName1
                )
            ),
            self.When(
                CreateRace(
                    self.testId,
                    self.RaceName1
                )
            ),
            self.ThenFailWith(RaceAlreadyCreated)
        )

    def test_can_change_race_name(self):
        self.Test(
            self.Given(
                RaceCreated(
                    self.testId,
                    self.RaceName1
                )
            ),
            self.When(
                ChangeRaceName(
                    self.testId,
                    self.RaceName2
                )
            ),
            self.Then(
                RaceNameChanged(
                    self.testId,
                    self.RaceName1,
                    self.RaceName2
                )
            )
        )

    def test_can_change_race_name_more_than_once(self):
        self.Test(
            self.Given(
                RaceCreated(
                    self.testId,
                    self.RaceName1
                ),
                RaceNameChanged(
                    self.testId,
                    self.RaceName1,
                    self.RaceName2
                )
            ),
            self.When(
                ChangeRaceName(
                    self.testId,
                    self.RaceName1
                )
            ),
            self.Then(
                RaceNameChanged(
                    self.testId,
                    self.RaceName2,
                    self.RaceName1
                )
            )
        )

    def test_cannot_change_uncreated_race_name(self):
        self.Test(
            self.Given(),
            self.When(
                ChangeRaceName(
                    self.testId,
                    self.RaceName1
                )
            ),
            self.ThenFailWith(RaceDoesNotExist)
        )

    def test_cannot_change_race_name_to_current_race_name(self):
        self.Test(
            self.Given(
                RaceCreated(
                    self.testId,
                    self.RaceName1
                )
            ),
            self.When(
                ChangeRaceName(
                    self.testId,
                    self.RaceName1
                )
            ),
            self.ThenFailWith(RaceNameDoesNotDiffer)
        )

    def test_can_add_subrace(self):
        self.Test(
            self.Given(
                RaceCreated(
                    self.testId,
                    self.RaceName1
                )
            ),
            self.When(
                Addsubrace(
                    self.testId,
                    self.subraceName1
                )
            ),
            self.Then(
                subraceAdded(
                    self.testId,
                    self.subraceName1
                )
            )
        )

    def test_cannot_add_subrace_to_uncreated_race(self):
        self.Test(
            self.Given(),
            self.When(
                Addsubrace(
                    self.testId,
                    self.subraceName1
                )
            ),
            self.ThenFailWith(RaceDoesNotExist)
        )

    def test_can_add_multiple_subraces(self):
        self.Test(
            self.Given(
                RaceCreated(
                    self.testId,
                    self.RaceName1
                ),
                subraceAdded(
                    self.testId,
                    self.subraceName1
                )
            ),
            self.When(
                Addsubrace(
                    self.testId,
                    self.subraceName2
                )
            ),
            self.Then(
                subraceAdded(
                    self.testId,
                    self.subraceName2
                )
            )
        )

    def test_cannot_add_same_subrace_more_than_once(self):
        self.Test(
            self.Given(
                RaceCreated(
                    self.testId,
                    self.RaceName1
                ),
                subraceAdded(
                    self.testId,
                    self.subraceName1
                )
            ),
            self.When(
                Addsubrace(
                    self.testId,
                    self.subraceName1
                )
            ),
            self.ThenFailWith(subraceAlreadyExists)
        )

    def test_can_remove_subrace(self):
        self.Test(
            self.Given(
                RaceCreated(
                    self.testId,
                    self.RaceName1
                ),
                subraceAdded(
                    self.testId,
                    self.subraceName1
                )
            ),
            self.When(
                Removesubrace(
                    self.testId,
                    self.subraceName1
                )
            ),
            self.Then(
                subraceRemoved(
                    self.testId,
                    self.subraceName1
                )
            )
        )

    def test_can_add_removed_subrace(self):
        self.Test(
            self.Given(
                RaceCreated(
                    self.testId,
                    self.RaceName1
                ),
                subraceAdded(
                    self.testId,
                    self.subraceName1
                ),
                subraceRemoved(
                    self.testId,
                    self.subraceName1
                )
            ),
            self.When(
                Addsubrace(
                    self.testId,
                    self.subraceName1
                )
            ),
            self.Then(
                subraceAdded(
                    self.testId,
                    self.subraceName1
                )
            )
        )

    def test_cannot_removed_subrace_more_than_once(self):
        self.Test(
            self.Given(
                RaceCreated(
                    self.testId,
                    self.RaceName1
                ),
                subraceAdded(
                    self.testId,
                    self.subraceName1
                ),
                subraceRemoved(
                    self.testId,
                    self.subraceName1
                )
            ),
            self.When(
                Removesubrace(
                    self.testId,
                    self.subraceName1
                )
            ),
            self.ThenFailWith(subraceDoesNotExists)
        )

    def test_can_rename_subrace(self):
        self.Test(
            self.Given(
                RaceCreated(
                    self.testId,
                    self.RaceName1
                ),
                subraceAdded(
                    self.testId,
                    self.subraceName1
                )
            ),
            self.When(
                Renamesubrace(
                    self.testId,
                    self.subraceName1,
                    self.subraceName2
                )
            ),
            self.Then(
                subraceRenamed(
                    self.testId,
                    self.subraceName1,
                    self.subraceName2
                )
            )
        )

    def test_can_rename_subrace_more_than_once(self):
        self.Test(
            self.Given(
                RaceCreated(
                    self.testId,
                    self.RaceName1
                ),
                subraceAdded(
                    self.testId,
                    self.subraceName1
                ),
                subraceRenamed(
                    self.testId,
                    self.subraceName1,
                    self.subraceName2
                )
            ),
            self.When(
                Renamesubrace(
                    self.testId,
                    self.subraceName2,
                    self.subraceName1
                )
            ),
            self.Then(
                subraceRenamed(
                    self.testId,
                    self.subraceName2,
                    self.subraceName1
                )
            )
        )

    def test_cannot_rename_unadded_subrace(self):
        self.Test(
            self.Given(
                RaceCreated(
                    self.testId,
                    self.RaceName1
                )
            ),
            self.When(
                Renamesubrace(
                    self.testId,
                    self.subraceName1,
                    self.subraceName2
                )
            ),
            self.ThenFailWith(subraceDoesNotExists)
        )

    def test_can_set_race_ability_modifiers(self):
        self.Test(
            self.Given(
                RaceCreated(
                    self.testId,
                    self.RaceName1
                )
            ),
            self.When(
                SetRaceAbilityModifiers(
                    self.testId,
                    []
                )
            ),
            self.Then(
                RaceAbilityModifiersSet(
                    self.testId,
                    []
                )
            )
        )

if __name__ == '__main__':
    unittest.main()
