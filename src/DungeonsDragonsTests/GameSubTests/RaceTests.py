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
    RaceCannotBeBasedOnSelf,
    RaceDoesNotExist,
    RaceNameDoesNotDiffer,
    subraceNameDoesNotDifferFromBaseRace,
    subraceAlreadyExists,
    subraceDoesNotExists
)
import uuid
import unittest


class RaceTests(BDDTest):

    def setUp(self):
        self.sut = RaceAggregate()
        self.RaceId = uuid.uuid1()
        self.SubraceId = uuid.uuid1()
        self.RaceName1 = 'Test Race 1'
        self.RaceName2 = 'Test Race 2'
        self.SubraceName1 = 'Test Subrace 1'
        self.SubraceName2 = 'Test Subrace 2'

    def test_can_create_race(self):
        self.Test(
            self.Given(),
            self.When(
                CreateRace(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.Then(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            )
        )

    def test_cannot_create_same_race_more_than_once(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                CreateRace(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.ThenFailWith(RaceAlreadyCreated)
        )

    def test_can_create_race_based_on_other(self):
        self.Test(
            self.Given(),
            self.When(
                CreateRace(
                    Id=self.SubraceId,
                    BaseRaceId=self.RaceId,

                )
            ),
            self.Then(
                RaceCreated(
                    Id=self.SubraceId,
                    BaseRaceId=self.RaceId
                )
            )
        )

    def test_cannot_create_race_based_on_self(self):
        self.Test(
            self.Given(),
            self.When(
                CreateRace(
                    Id=self.RaceId,
                    BaseRaceId=self.RaceId,

                )
            ),
            self.ThenFailWith(RaceCannotBeBasedOnSelf)
        )

    # def test_can_change_race_name(self):
    #     self.Test(
    #         self.Given(
    #             RaceCreated(
    #                 self.RaceId,
    #                 self.RaceName1
    #             )
    #         ),
    #         self.When(
    #             ChangeRaceName(
    #                 self.RaceId,
    #                 self.RaceName2
    #             )
    #         ),
    #         self.Then(
    #             RaceNameChanged(
    #                 self.RaceId,
    #                 self.RaceName1,
    #                 self.RaceName2
    #             )
    #         )
    #     )

    # def test_can_change_race_name_more_than_once(self):
    #     self.Test(
    #         self.Given(
    #             RaceCreated(
    #                 self.RaceId,
    #                 self.RaceName1
    #             ),
    #             RaceNameChanged(
    #                 self.RaceId,
    #                 self.RaceName1,
    #                 self.RaceName2
    #             )
    #         ),
    #         self.When(
    #             ChangeRaceName(
    #                 self.RaceId,
    #                 self.RaceName1
    #             )
    #         ),
    #         self.Then(
    #             RaceNameChanged(
    #                 self.RaceId,
    #                 self.RaceName2,
    #                 self.RaceName1
    #             )
    #         )
    #     )

    # def test_cannot_change_uncreated_race_name(self):
    #     self.Test(
    #         self.Given(),
    #         self.When(
    #             ChangeRaceName(
    #                 self.RaceId,
    #                 self.RaceName1
    #             )
    #         ),
    #         self.ThenFailWith(RaceDoesNotExist)
    #     )

    # def test_cannot_change_race_name_to_current_race_name(self):
    #     self.Test(
    #         self.Given(
    #             RaceCreated(
    #                 self.RaceId,
    #                 self.RaceName1
    #             )
    #         ),
    #         self.When(
    #             ChangeRaceName(
    #                 self.RaceId,
    #                 self.RaceName1
    #             )
    #         ),
    #         self.ThenFailWith(RaceNameDoesNotDiffer)
    #     )

    # def test_can_add_subrace(self):
    #     self.Test(
    #         self.Given(
    #             RaceCreated(
    #                 self.RaceId,
    #                 self.RaceName1
    #             )
    #         ),
    #         self.When(
    #             Addsubrace(
    #                 self.RaceId,
    #                 self.subraceName1
    #             )
    #         ),
    #         self.Then(
    #             subraceAdded(
    #                 self.RaceId,
    #                 self.subraceName1
    #             )
    #         )
    #     )

    # def test_cannot_add_subrace_to_uncreated_race(self):
    #     self.Test(
    #         self.Given(),
    #         self.When(
    #             Addsubrace(
    #                 self.RaceId,
    #                 self.subraceName1
    #             )
    #         ),
    #         self.ThenFailWith(RaceDoesNotExist)
    #     )

    # def test_can_add_multiple_subraces(self):
    #     self.Test(
    #         self.Given(
    #             RaceCreated(
    #                 self.RaceId,
    #                 self.RaceName1
    #             ),
    #             subraceAdded(
    #                 self.RaceId,
    #                 self.subraceName1
    #             )
    #         ),
    #         self.When(
    #             Addsubrace(
    #                 self.RaceId,
    #                 self.subraceName2
    #             )
    #         ),
    #         self.Then(
    #             subraceAdded(
    #                 self.RaceId,
    #                 self.subraceName2
    #             )
    #         )
    #     )

    # def test_cannot_add_same_subrace_more_than_once(self):
    #     self.Test(
    #         self.Given(
    #             RaceCreated(
    #                 self.RaceId,
    #                 self.RaceName1
    #             ),
    #             subraceAdded(
    #                 self.RaceId,
    #                 self.subraceName1
    #             )
    #         ),
    #         self.When(
    #             Addsubrace(
    #                 self.RaceId,
    #                 self.subraceName1
    #             )
    #         ),
    #         self.ThenFailWith(subraceAlreadyExists)
    #     )

    # def test_can_remove_subrace(self):
    #     self.Test(
    #         self.Given(
    #             RaceCreated(
    #                 self.RaceId,
    #                 self.RaceName1
    #             ),
    #             subraceAdded(
    #                 self.RaceId,
    #                 self.subraceName1
    #             )
    #         ),
    #         self.When(
    #             Removesubrace(
    #                 self.RaceId,
    #                 self.subraceName1
    #             )
    #         ),
    #         self.Then(
    #             subraceRemoved(
    #                 self.RaceId,
    #                 self.subraceName1
    #             )
    #         )
    #     )

    # def test_can_add_removed_subrace(self):
    #     self.Test(
    #         self.Given(
    #             RaceCreated(
    #                 self.RaceId,
    #                 self.RaceName1
    #             ),
    #             subraceAdded(
    #                 self.RaceId,
    #                 self.subraceName1
    #             ),
    #             subraceRemoved(
    #                 self.RaceId,
    #                 self.subraceName1
    #             )
    #         ),
    #         self.When(
    #             Addsubrace(
    #                 self.RaceId,
    #                 self.subraceName1
    #             )
    #         ),
    #         self.Then(
    #             subraceAdded(
    #                 self.RaceId,
    #                 self.subraceName1
    #             )
    #         )
    #     )

    # def test_cannot_removed_subrace_more_than_once(self):
    #     self.Test(
    #         self.Given(
    #             RaceCreated(
    #                 self.RaceId,
    #                 self.RaceName1
    #             ),
    #             subraceAdded(
    #                 self.RaceId,
    #                 self.subraceName1
    #             ),
    #             subraceRemoved(
    #                 self.RaceId,
    #                 self.subraceName1
    #             )
    #         ),
    #         self.When(
    #             Removesubrace(
    #                 self.RaceId,
    #                 self.subraceName1
    #             )
    #         ),
    #         self.ThenFailWith(subraceDoesNotExists)
    #     )

    # def test_can_rename_subrace(self):
    #     self.Test(
    #         self.Given(
    #             RaceCreated(
    #                 self.RaceId,
    #                 self.RaceName1
    #             ),
    #             subraceAdded(
    #                 self.RaceId,
    #                 self.subraceName1
    #             )
    #         ),
    #         self.When(
    #             Renamesubrace(
    #                 self.RaceId,
    #                 self.subraceName1,
    #                 self.subraceName2
    #             )
    #         ),
    #         self.Then(
    #             subraceRenamed(
    #                 self.RaceId,
    #                 self.subraceName1,
    #                 self.subraceName2
    #             )
    #         )
    #     )

    # def test_can_rename_subrace_more_than_once(self):
    #     self.Test(
    #         self.Given(
    #             RaceCreated(
    #                 self.RaceId,
    #                 self.RaceName1
    #             ),
    #             subraceAdded(
    #                 self.RaceId,
    #                 self.subraceName1
    #             ),
    #             subraceRenamed(
    #                 self.RaceId,
    #                 self.subraceName1,
    #                 self.subraceName2
    #             )
    #         ),
    #         self.When(
    #             Renamesubrace(
    #                 self.RaceId,
    #                 self.subraceName2,
    #                 self.subraceName1
    #             )
    #         ),
    #         self.Then(
    #             subraceRenamed(
    #                 self.RaceId,
    #                 self.subraceName2,
    #                 self.subraceName1
    #             )
    #         )
    #     )

    # def test_cannot_rename_unadded_subrace(self):
    #     self.Test(
    #         self.Given(
    #             RaceCreated(
    #                 self.RaceId,
    #                 self.RaceName1
    #             )
    #         ),
    #         self.When(
    #             Renamesubrace(
    #                 self.RaceId,
    #                 self.subraceName1,
    #                 self.subraceName2
    #             )
    #         ),
    #         self.ThenFailWith(subraceDoesNotExists)
    #     )

    # def test_can_set_race_ability_modifiers(self):
    #     self.Test(
    #         self.Given(
    #             RaceCreated(
    #                 self.RaceId,
    #                 self.RaceName1
    #             )
    #         ),
    #         self.When(
    #             SetRaceAbilityModifiers(
    #                 self.RaceId,
    #                 []
    #             )
    #         ),
    #         self.Then(
    #             RaceAbilityModifiersSet(
    #                 self.RaceId,
    #                 []
    #             )
    #         )
    #     )


if __name__ == '__main__':
    unittest.main()
