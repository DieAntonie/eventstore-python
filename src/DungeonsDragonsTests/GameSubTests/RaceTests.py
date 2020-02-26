from ...Infrastructure.BDDTest import BDDTest
from ...DungeonsDragons.Game.Race.RaceAggregate import RaceAggregate
from ...DungeonsDragons.Game.Ability import Ability
from ...DungeonsDragons.Game.Race.Commands import (
    CreateRace,
    SetRaceDetails,
    SetRaceAbilityScoreIncrease,
    SetRaceAge
)
from ...DungeonsDragons.Game.Race.Events import (
    RaceCreated,
    RaceNameSet,
    RaceDescriptionSet,
    RaceAbilityScoreIncreaseSet,
    RaceMaturityAgeSet,
    RaceLifeExpectancySet
)
from ...DungeonsDragons.Game.Race.Exceptions import (
    RaceAlreadyCreated,
    RaceCannotBeBasedOnSelf,
    RaceDoesNotExist,
    TooManyOtherAbilityScoreIncreaseTokens,
    InvalidAbilityScoreIncreaseTokenStructure,
    InvalidAbilityScoreIncreaseToken,
    RaceMaturityAgeExceedsLifeExpectency,
    RaceMaturityAgeTooSmall
)
import uuid
import unittest


class RaceTests(BDDTest):

    def setUp(self):
        self.sut = RaceAggregate()
        self.RaceId = uuid.uuid1()
        self.SubraceId = uuid.uuid1()
        self.RaceName1 = 'Race 1'
        self.RaceName2 = 'Race 2'
        self.RaceDescription1 = 'Description 1'
        self.RaceDescription2 = 'Description 2'
        self.ValidAbilityScoreIncrease = [
            {Ability.Strength.value: 2},
            {Ability.Intelligence.value: 1},
            {Ability.Any.value: 1},
            {Ability.Other.value: 1}
        ]
        self.InvalidAbilityScoreIncrease = [
            {Ability.Strength.value: 2},
            {Ability.Dexterity.value: 1},
            {Ability.Constitution.value: 1},
            {Ability.Any.value: 1},
            {Ability.Other.value: 1},
            {Ability.Other.value: 1},
            {Ability.Other.value: 1}
        ]
        self.InvalidAbilityScoreIncreaseTokenStructure = [
            {
                Ability.Strength.value: 2,
                Ability.Dexterity.value: 1
            }
        ]
        self.InvalidAbilityScoreIncreaseToken = [
            {Ability.Strength.value: 2},
            {'value': 1}
        ]
        self.MaturityAge1 = 19
        self.MaturityAge2 = 75
        self.LifeExpectencyAge1 = 100
        self.LifeExpectencyAge2 = 50
        self.ZeroAge = 0

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

    def test_can_set_race_details_unchanged(self):
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
                    Description=self.RaceDescription1
                )
            ),
            self.Then()
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

    def test_can_set_race_ability_score_increase(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                SetRaceAbilityScoreIncrease(
                    Id=self.RaceId,
                    AbilityScoreIncrease=self.ValidAbilityScoreIncrease
                )
            ),
            self.Then(
                RaceAbilityScoreIncreaseSet(
                    Id=self.RaceId,
                    AbilityScoreIncrease=self.ValidAbilityScoreIncrease
                )
            )
        )

    def test_can_set_race_ability_score_increase_unchanged(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceAbilityScoreIncreaseSet(
                    Id=self.RaceId,
                    AbilityScoreIncrease=self.ValidAbilityScoreIncrease
                )
            ),
            self.When(
                SetRaceAbilityScoreIncrease(
                    Id=self.RaceId,
                    AbilityScoreIncrease=self.ValidAbilityScoreIncrease
                )
            ),
            self.Then()
        )

    def test_cannot_set_race_ability_score_increase_with_Other_tokens_equal_to_or_more_than_available_abilities(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                SetRaceAbilityScoreIncrease(
                    Id=self.RaceId,
                    AbilityScoreIncrease=self.InvalidAbilityScoreIncrease
                )
            ),
            self.ThenFailWith(TooManyOtherAbilityScoreIncreaseTokens)
        )
        
    def test_cannot_set_race_ability_score_increase_with_invalid_token_structure(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                SetRaceAbilityScoreIncrease(
                    Id=self.RaceId,
                    AbilityScoreIncrease=self.InvalidAbilityScoreIncreaseTokenStructure
                )
            ),
            self.ThenFailWith(InvalidAbilityScoreIncreaseTokenStructure)
        )
        
    def test_cannot_set_race_ability_score_increase_with_invalid_token(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                SetRaceAbilityScoreIncrease(
                    Id=self.RaceId,
                    AbilityScoreIncrease=self.InvalidAbilityScoreIncreaseToken
                )
            ),
            self.ThenFailWith(InvalidAbilityScoreIncreaseToken)
        )

    def test_cannot_set_uncreated_race_ability_score_increase(self):
        self.Test(
            self.Given(),
            self.When(
                SetRaceAbilityScoreIncrease(
                    Id=self.RaceId,
                    AbilityScoreIncrease=self.ValidAbilityScoreIncrease
                )
            ),
            self.ThenFailWith(RaceDoesNotExist)
        )

    def test_can_set_race_age(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                SetRaceAge(
                    Id=self.RaceId,
                    MaturityAge=self.MaturityAge1,
                    LifeExpectency=self.LifeExpectencyAge1
                )
            ),
            self.Then(
                RaceMaturityAgeSet(
                    Id=self.RaceId,
                    MaturityAge=self.MaturityAge1
                ),
                RaceLifeExpectancySet(
                    Id=self.RaceId,
                    LifeExpectency=self.LifeExpectencyAge1
                )
            )
        )

    def test_can_set_race_age_unchanged(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceMaturityAgeSet(
                    Id=self.RaceId,
                    MaturityAge=self.MaturityAge1
                ),
                RaceLifeExpectancySet(
                    Id=self.RaceId,
                    LifeExpectency=self.LifeExpectencyAge1
                )
            ),
            self.When(
                SetRaceAge(
                    Id=self.RaceId,
                    MaturityAge=self.MaturityAge1,
                    LifeExpectency=self.LifeExpectencyAge1
                )
            ),
            self.Then()
        )

    def test_can_set_race_age_same_life_expectency(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceMaturityAgeSet(
                    Id=self.RaceId,
                    MaturityAge=self.MaturityAge1
                ),
                RaceLifeExpectancySet(
                    Id=self.RaceId,
                    LifeExpectency=self.LifeExpectencyAge1
                )
            ),
            self.When(
                SetRaceAge(
                    Id=self.RaceId,
                    MaturityAge=self.MaturityAge2,
                    LifeExpectency=self.LifeExpectencyAge1
                )
            ),
            self.Then(
                RaceMaturityAgeSet(
                    Id=self.RaceId,
                    MaturityAge=self.MaturityAge2
                )
            )
        )

    def test_can_set_race_age_same_maturity_age(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceMaturityAgeSet(
                    Id=self.RaceId,
                    MaturityAge=self.MaturityAge1
                ),
                RaceLifeExpectancySet(
                    Id=self.RaceId,
                    LifeExpectency=self.LifeExpectencyAge1
                )
            ),
            self.When(
                SetRaceAge(
                    Id=self.RaceId,
                    MaturityAge=self.MaturityAge1,
                    LifeExpectency=self.LifeExpectencyAge2
                )
            ),
            self.Then(
                RaceLifeExpectancySet(
                    Id=self.RaceId,
                    LifeExpectency=self.LifeExpectencyAge2
                )
            )
        )

    def test_cannot_set_race_with_maturity_age_equal_or_greater_than_life_expectency(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                SetRaceAge(
                    Id=self.RaceId,
                    MaturityAge=self.MaturityAge2,
                    LifeExpectency=self.LifeExpectencyAge2
                )
            ),
            self.ThenFailWith(RaceMaturityAgeExceedsLifeExpectency)
        )

    def test_cannot_set_race_with_maturity_age_less_then_one(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                SetRaceAge(
                    Id=self.RaceId,
                    MaturityAge=self.ZeroAge,
                    LifeExpectency=self.LifeExpectencyAge1
                )
            ),
            self.ThenFailWith(RaceMaturityAgeTooSmall)
        )

    def test_cannot_set_race_with_maturity_age_less_then_one(self):
        self.Test(
            self.Given(),
            self.When(
                SetRaceAge(
                    Id=self.RaceId,
                    MaturityAge=self.MaturityAge1,
                    LifeExpectency=self.LifeExpectencyAge1
                )
            ),
            self.ThenFailWith(RaceDoesNotExist)
        )


if __name__ == '__main__':
    unittest.main()
