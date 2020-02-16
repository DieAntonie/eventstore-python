from ...Infrastructure.BDDTest import BDDTest
from ...DungeonsDragons.Game.Race.RaceAggregate import RaceAggregate
from ...DungeonsDragons.Game.Race.Commands import (
    CreateRace,
    SetRaceDetails
)
from ...DungeonsDragons.Game.Race.Events import (
    RaceCreated,
    RaceNameSet,
    RaceDescriptionSet
)
from ...DungeonsDragons.Game.Race.Exceptions import (
    RaceAlreadyCreated,
    RaceCannotBeBasedOnSelf,
    RaceDoesNotExist
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
        self.RaceDescription1 = 'This is a description and background of Race 1'
        self.RaceDescription2 = 'This is a description and background of Race 2'
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

    def test_can_set_race_details(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                SetRaceDetails(
                    Id=self.RaceId,
                    Name=self.RaceName1,
                    Description=self.RaceDescription1
                )
            ),
            self.Then(
                RaceNameSet(
                    Id=self.RaceId,
                    Name=self.RaceName1
                ),
                RaceDescriptionSet(
                    Id=self.RaceId,
                    Description=self.RaceDescription1
                )
            )
        )

    def test_can_set_race_details_with_same_name(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceNameSet(
                    Id=self.RaceId,
                    Name=self.RaceName1
                ),
                RaceDescriptionSet(
                    Id=self.RaceId,
                    Description=self.RaceDescription1
                )
            ),
            self.When(
                SetRaceDetails(
                    Id=self.RaceId,
                    Name=self.RaceName1,
                    Description=self.RaceDescription2
                )
            ),
            self.Then(
                RaceDescriptionSet(
                    Id=self.RaceId,
                    Description=self.RaceDescription2
                )
            )
        )

    def test_can_set_race_details_with_same_description(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceNameSet(
                    Id=self.RaceId,
                    Name=self.RaceName1
                ),
                RaceDescriptionSet(
                    Id=self.RaceId,
                    Description=self.RaceDescription1
                )
            ),
            self.When(
                SetRaceDetails(
                    Id=self.RaceId,
                    Name=self.RaceName2,
                    Description=self.RaceDescription1
                )
            ),
            self.Then(
                RaceNameSet(
                    Id=self.RaceId,
                    Name=self.RaceName2
                )
            )
        )

    def test_cannot_set_uncreated_race_details(self):
        self.Test(
            self.Given(),
            self.When(
                SetRaceDetails(
                    Id=self.RaceId,
                    Name=self.RaceName1,
                    Description=self.RaceDescription1
                )
            ),
            self.ThenFailWith(RaceDoesNotExist)
        )


if __name__ == '__main__':
    unittest.main()
