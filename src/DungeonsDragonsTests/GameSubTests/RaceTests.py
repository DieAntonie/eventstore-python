from ...Infrastructure.BDDTest import BDDTest
from ...DungeonsDragons.Game.Ability import Ability
from ...DungeonsDragons.Game.Length import Foot
from ...DungeonsDragons.Game.Race.RaceAggregate import RaceAggregate
from ...DungeonsDragons.Game.SizeCategory import SizeCategory
from ...DungeonsDragons.Game.DiceRoll import (
    Dice,
    DiceRoll
)
from ...DungeonsDragons.Game.Race.Commands import (
    CreateRace,
    SetRaceDetails,
    SetRaceAbilityScoreIncrease,
    SetRaceAge,
    SetRaceAlignment,
    SetRaceSize,
    SetRaceSpeed,
    SetRaceLanguages,
    SetRaceSubRaces
)
from ...DungeonsDragons.Game.Race.Events import (
    RaceCreated,
    RaceNameSet,
    RaceDescriptionSet,
    RaceAbilityScoreIncreaseSet,
    RaceMaturityAgeSet,
    RaceLifeExpectancySet,
    RaceOrthodoxySet,
    RaceMoralitySet,
    RaceSizeCategorySet,
    RaceBaseHeightSet,
    RaceHeightModifierSet,
    RaceBaseWeightSet,
    RaceWeightModifierSet,
    RaceBaseWalkSpeedSet,
    RaceLanguagesSet,
    RaceSubRacesSet
)
from ...DungeonsDragons.Game.Race.Exceptions import (
    RaceAlreadyCreated,
    RaceCannotBeBasedOnSelf,
    RaceDoesNotExist,
    TooManyOtherAbilityScoreIncreaseTokens,
    InvalidAbilityScoreIncreaseTokenStructure,
    InvalidAbilityScoreIncreaseToken,
    RaceMaturityAgeExceedsLifeExpectency,
    RaceMaturityAgeTooSmall,
    RaceOrthodoxyOutsideAllowedSpectrum,
    RaceMoralityOutsideAllowedSpectrum
)
from ...DungeonsDragons.Game.Language import Language
import uuid
import unittest


class RaceTests(BDDTest):

    def setUp(self):
        self.sut = RaceAggregate()
        self.RaceId = uuid.uuid1()
        self.Subrace1Id = uuid.uuid1()
        self.Subrace2Id = uuid.uuid1()
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
        self.Lawful = self.Good = 1
        self.Chaotic = self.Evil = -1
        self.OverlyChaotic = self.OverlyEvil = -1.1
        self.OverlyLawful = self.OverlyGood = 1.1
        self.MediumSize = SizeCategory.Medium
        self.LargeSize = SizeCategory.Large
        self.FourFootEight = Foot(4, 8)
        self.ThreeFootSeven = Foot(3, 7)
        self.TwoTenSidedDie = DiceRoll(2, Dice.TenSidedDie)
        self.ThreeFourSidedDie = DiceRoll(3, Dice.FourSidedDie)
        self.HundredAndTenPounds = 110
        self.SeventyFivePounds = 75
        self.ThirtyFeet = Foot(30)
        self.TwentyFiveFeet = Foot(25)
        self.Monoglot = [Language.Common]
        self.Polyglot = [Language.Common, Language.Dwarvish]


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
                    Id=self.Subrace1Id,
                    BaseRaceId=self.RaceId,
                )
            ),
            self.Then(
                RaceCreated(
                    Id=self.Subrace1Id,
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

    def test_cannot_set_uncreated_race_age(self):
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

    def test_can_set_race_alignment(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                SetRaceAlignment(
                    Id=self.RaceId,
                    Orthodoxy=self.Lawful,
                    Morality=self.Good
                )
            ),
            self.Then(
                RaceOrthodoxySet(
                    Id=self.RaceId,
                    Orthodoxy=self.Lawful
                ),
                RaceMoralitySet(
                    Id=self.RaceId,
                    Morality=self.Good
                )
            )
        )

    def test_can_set_race_alignment_unchanged(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceOrthodoxySet(
                    Id=self.RaceId,
                    Orthodoxy=self.Lawful
                ),
                RaceMoralitySet(
                    Id=self.RaceId,
                    Morality=self.Good
                )
            ),
            self.When(
                SetRaceAlignment(
                    Id=self.RaceId,
                    Orthodoxy=self.Lawful,
                    Morality=self.Good
                )
            ),
            self.Then()
        )

    def test_can_set_race_alignment_with_same_morality(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceOrthodoxySet(
                    Id=self.RaceId,
                    Orthodoxy=self.Lawful
                ),
                RaceMoralitySet(
                    Id=self.RaceId,
                    Morality=self.Good
                )
            ),
            self.When(
                SetRaceAlignment(
                    Id=self.RaceId,
                    Orthodoxy=self.Chaotic,
                    Morality=self.Good
                )
            ),
            self.Then(
                RaceOrthodoxySet(
                    Id=self.RaceId,
                    Orthodoxy=self.Chaotic
                )
            )
        )

    def test_can_set_race_alignment_with_same_orthodoxy(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceOrthodoxySet(
                    Id=self.RaceId,
                    Orthodoxy=self.Lawful
                ),
                RaceMoralitySet(
                    Id=self.RaceId,
                    Morality=self.Good
                )
            ),
            self.When(
                SetRaceAlignment(
                    Id=self.RaceId,
                    Orthodoxy=self.Lawful,
                    Morality=self.Evil
                )
            ),
            self.Then(
                RaceMoralitySet(
                    Id=self.RaceId,
                    Morality=self.Evil
                )
            )
        )

    def test_cannot_set_race_alignment_with_outer_spectrum_orthodoxy(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                SetRaceAlignment(
                    Id=self.RaceId,
                    Orthodoxy=self.OverlyChaotic,
                    Morality=self.Good
                )
            ),
            self.ThenFailWith(RaceOrthodoxyOutsideAllowedSpectrum)
        )
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                SetRaceAlignment(
                    Id=self.RaceId,
                    Orthodoxy=self.OverlyLawful,
                    Morality=self.Good
                )
            ),
            self.ThenFailWith(RaceOrthodoxyOutsideAllowedSpectrum)
        )

    def test_cannot_set_race_alignment_with_outer_spectrum_morality(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                SetRaceAlignment(
                    Id=self.RaceId,
                    Orthodoxy=self.Lawful,
                    Morality=self.OverlyGood
                )
            ),
            self.ThenFailWith(RaceMoralityOutsideAllowedSpectrum)
        )
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                SetRaceAlignment(
                    Id=self.RaceId,
                    Orthodoxy=self.Lawful,
                    Morality=self.OverlyEvil
                )
            ),
            self.ThenFailWith(RaceMoralityOutsideAllowedSpectrum)
        )

    def test_cannot_set_uncreated_race_alignment(self):
        self.Test(
            self.Given(),
            self.When(
                SetRaceAlignment(
                    Id=self.RaceId,
                    Orthodoxy=self.Lawful,
                    Morality=self.Good
                )
            ),
            self.ThenFailWith(RaceDoesNotExist)
        )

    def test_can_set_race_size(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                SetRaceSize(
                    Id=self.RaceId,
                    SizeCategory=self.MediumSize,
                    BaseHeight=self.FourFootEight,
                    HeightModifier=self.TwoTenSidedDie,
                    BaseWeight=self.HundredAndTenPounds,
                    WeightModifier=self.ThreeFourSidedDie
                )
            ),
            self.Then(
                RaceSizeCategorySet(
                    Id=self.RaceId,
                    SizeCategory=self.MediumSize
                ),
                RaceBaseHeightSet(
                    Id=self.RaceId,
                    BaseHeight=self.FourFootEight
                ),
                RaceHeightModifierSet(
                    Id=self.RaceId,
                    HeightModifier=self.TwoTenSidedDie
                ),
                RaceBaseWeightSet(
                    Id=self.RaceId,
                    BaseWeight=self.HundredAndTenPounds
                ),
                RaceWeightModifierSet(
                    Id=self.RaceId,
                    WeightModifier=self.ThreeFourSidedDie
                )
            )
        )

    def test_can_set_race_size_with_unchanged_values(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceSizeCategorySet(
                    Id=self.RaceId,
                    SizeCategory=self.MediumSize
                ),
                RaceBaseHeightSet(
                    Id=self.RaceId,
                    BaseHeight=self.FourFootEight
                ),
                RaceHeightModifierSet(
                    Id=self.RaceId,
                    HeightModifier=self.TwoTenSidedDie
                ),
                RaceBaseWeightSet(
                    Id=self.RaceId,
                    BaseWeight=self.HundredAndTenPounds
                ),
                RaceWeightModifierSet(
                    Id=self.RaceId,
                    WeightModifier=self.ThreeFourSidedDie
                )
            ),
            self.When(
                SetRaceSize(
                    Id=self.RaceId,
                    SizeCategory=self.MediumSize,
                    BaseHeight=self.FourFootEight,
                    HeightModifier=self.TwoTenSidedDie,
                    BaseWeight=self.HundredAndTenPounds,
                    WeightModifier=self.ThreeFourSidedDie
                )
            ),
            self.Then()
        )

        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceSizeCategorySet(
                    Id=self.RaceId,
                    SizeCategory=self.MediumSize
                ),
                RaceBaseHeightSet(
                    Id=self.RaceId,
                    BaseHeight=self.FourFootEight
                ),
                RaceHeightModifierSet(
                    Id=self.RaceId,
                    HeightModifier=self.TwoTenSidedDie
                ),
                RaceBaseWeightSet(
                    Id=self.RaceId,
                    BaseWeight=self.HundredAndTenPounds
                ),
                RaceWeightModifierSet(
                    Id=self.RaceId,
                    WeightModifier=self.ThreeFourSidedDie
                )
            ),
            self.When(
                SetRaceSize(
                    Id=self.RaceId,
                    SizeCategory=self.LargeSize,
                    BaseHeight=self.FourFootEight,
                    HeightModifier=self.TwoTenSidedDie,
                    BaseWeight=self.HundredAndTenPounds,
                    WeightModifier=self.ThreeFourSidedDie
                )
            ),
            self.Then(
                RaceSizeCategorySet(
                    Id=self.RaceId,
                    SizeCategory=self.LargeSize
                )
            )
        )

        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceSizeCategorySet(
                    Id=self.RaceId,
                    SizeCategory=self.MediumSize
                ),
                RaceBaseHeightSet(
                    Id=self.RaceId,
                    BaseHeight=self.FourFootEight
                ),
                RaceHeightModifierSet(
                    Id=self.RaceId,
                    HeightModifier=self.TwoTenSidedDie
                ),
                RaceBaseWeightSet(
                    Id=self.RaceId,
                    BaseWeight=self.HundredAndTenPounds
                ),
                RaceWeightModifierSet(
                    Id=self.RaceId,
                    WeightModifier=self.ThreeFourSidedDie
                )
            ),
            self.When(
                SetRaceSize(
                    Id=self.RaceId,
                    SizeCategory=self.MediumSize,
                    BaseHeight=self.ThreeFootSeven,
                    HeightModifier=self.TwoTenSidedDie,
                    BaseWeight=self.HundredAndTenPounds,
                    WeightModifier=self.ThreeFourSidedDie
                )
            ),
            self.Then(
                RaceBaseHeightSet(
                    Id=self.RaceId,
                    BaseHeight=self.ThreeFootSeven
                )
            )
        )

        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceSizeCategorySet(
                    Id=self.RaceId,
                    SizeCategory=self.MediumSize
                ),
                RaceBaseHeightSet(
                    Id=self.RaceId,
                    BaseHeight=self.FourFootEight
                ),
                RaceHeightModifierSet(
                    Id=self.RaceId,
                    HeightModifier=self.TwoTenSidedDie
                ),
                RaceBaseWeightSet(
                    Id=self.RaceId,
                    BaseWeight=self.HundredAndTenPounds
                ),
                RaceWeightModifierSet(
                    Id=self.RaceId,
                    WeightModifier=self.ThreeFourSidedDie
                )
            ),
            self.When(
                SetRaceSize(
                    Id=self.RaceId,
                    SizeCategory=self.MediumSize,
                    BaseHeight=self.FourFootEight,
                    HeightModifier=self.ThreeFourSidedDie,
                    BaseWeight=self.HundredAndTenPounds,
                    WeightModifier=self.ThreeFourSidedDie
                )
            ),
            self.Then(
                RaceHeightModifierSet(
                    Id=self.RaceId,
                    HeightModifier=self.ThreeFourSidedDie
                )
            )
        )

        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceSizeCategorySet(
                    Id=self.RaceId,
                    SizeCategory=self.MediumSize
                ),
                RaceBaseHeightSet(
                    Id=self.RaceId,
                    BaseHeight=self.FourFootEight
                ),
                RaceHeightModifierSet(
                    Id=self.RaceId,
                    HeightModifier=self.TwoTenSidedDie
                ),
                RaceBaseWeightSet(
                    Id=self.RaceId,
                    BaseWeight=self.HundredAndTenPounds
                ),
                RaceWeightModifierSet(
                    Id=self.RaceId,
                    WeightModifier=self.ThreeFourSidedDie
                )
            ),
            self.When(
                SetRaceSize(
                    Id=self.RaceId,
                    SizeCategory=self.MediumSize,
                    BaseHeight=self.FourFootEight,
                    HeightModifier=self.TwoTenSidedDie,
                    BaseWeight=self.SeventyFivePounds,
                    WeightModifier=self.ThreeFourSidedDie
                )
            ),
            self.Then(
                RaceBaseWeightSet(
                    Id=self.RaceId,
                    BaseWeight=self.SeventyFivePounds
                )
            )
        )

        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceSizeCategorySet(
                    Id=self.RaceId,
                    SizeCategory=self.MediumSize
                ),
                RaceBaseHeightSet(
                    Id=self.RaceId,
                    BaseHeight=self.FourFootEight
                ),
                RaceHeightModifierSet(
                    Id=self.RaceId,
                    HeightModifier=self.TwoTenSidedDie
                ),
                RaceBaseWeightSet(
                    Id=self.RaceId,
                    BaseWeight=self.HundredAndTenPounds
                ),
                RaceWeightModifierSet(
                    Id=self.RaceId,
                    WeightModifier=self.ThreeFourSidedDie
                )
            ),
            self.When(
                SetRaceSize(
                    Id=self.RaceId,
                    SizeCategory=self.MediumSize,
                    BaseHeight=self.FourFootEight,
                    HeightModifier=self.TwoTenSidedDie,
                    BaseWeight=self.HundredAndTenPounds,
                    WeightModifier=self.TwoTenSidedDie
                )
            ),
            self.Then(
                RaceWeightModifierSet(
                    Id=self.RaceId,
                    WeightModifier=self.TwoTenSidedDie
                )
            )
        )

    def test_cannot_set_uncreated_race_size(self):
        self.Test(
            self.Given(),
            self.When(
                SetRaceSize(
                    Id=self.RaceId,
                    SizeCategory=self.MediumSize,
                    BaseHeight=self.FourFootEight,
                    HeightModifier=self.TwoTenSidedDie,
                    BaseWeight=self.HundredAndTenPounds,
                    WeightModifier=self.ThreeFourSidedDie
                )
            ),
            self.ThenFailWith(RaceDoesNotExist)
        )

    def test_can_set_race_speed(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                SetRaceSpeed(
                    Id=self.RaceId,
                    BaseWalkSpeed=self.ThirtyFeet
                )
            ),
            self.Then(
                RaceBaseWalkSpeedSet(
                    Id=self.RaceId,
                    BaseWalkSpeed=self.ThirtyFeet
                )
            )
        )

    def test_can_set_race_speed_unchanged(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceBaseWalkSpeedSet(
                    Id=self.RaceId,
                    BaseWalkSpeed=self.ThirtyFeet
                )
            ),
            self.When(
                SetRaceSpeed(
                    Id=self.RaceId,
                    BaseWalkSpeed=self.ThirtyFeet
                )
            ),
            self.Then()
        )

        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceBaseWalkSpeedSet(
                    Id=self.RaceId,
                    BaseWalkSpeed=self.ThirtyFeet
                )
            ),
            self.When(
                SetRaceSpeed(
                    Id=self.RaceId,
                    BaseWalkSpeed=self.TwentyFiveFeet
                )
            ),
            self.Then(
                RaceBaseWalkSpeedSet(
                    Id=self.RaceId,
                    BaseWalkSpeed=self.TwentyFiveFeet
                )
            )
        )

    def test_cannot_set_uncreated_race_speed(self):
        self.Test(
            self.Given(),
            self.When(
                SetRaceSpeed(
                    Id=self.RaceId,
                    BaseWalkSpeed=self.ThirtyFeet
                )
            ),
            self.ThenFailWith(RaceDoesNotExist)
        )

    def test_can_set_race_languages(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                SetRaceLanguages(
                    Id=self.RaceId,
                    Languages=self.Monoglot
                )
            ),
            self.Then(
                RaceLanguagesSet(
                    Id=self.RaceId,
                    Languages=self.Monoglot
                )
            )
        )

    def test_can_set_race_languages_unchanged(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceLanguagesSet(
                    Id=self.RaceId,
                    Languages=self.Monoglot
                )
            ),
            self.When(
                SetRaceLanguages(
                    Id=self.RaceId,
                    Languages=self.Monoglot
                )
            ),
            self.Then()
        )

        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceLanguagesSet(
                    Id=self.RaceId,
                    Languages=self.Monoglot
                )
            ),
            self.When(
                SetRaceLanguages(
                    Id=self.RaceId,
                    Languages=self.Polyglot
                )
            ),
            self.Then(
                RaceLanguagesSet(
                    Id=self.RaceId,
                    Languages=self.Polyglot
                )
            )
        )

    def test_cannot_set_uncreated_race_languages(self):
        self.Test(
            self.Given(),
            self.When(
                SetRaceLanguages(
                    Id=self.RaceId,
                    Languages=self.Monoglot
                )
            ),
            self.ThenFailWith(RaceDoesNotExist)
        )

    def test_can_set_race_sub_races(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                )
            ),
            self.When(
                SetRaceSubRaces(
                    Id=self.RaceId,
                    Subraces=[self.Subrace1Id]
                )
            ),
            self.Then(
                RaceSubRacesSet(
                    Id=self.RaceId,
                    Subraces=[self.Subrace1Id]
                )
            )
        )

    def test_can_set_race_sub_races_unchanged(self):
        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceSubRacesSet(
                    Id=self.RaceId,
                    Subraces=[self.Subrace1Id]
                )
            ),
            self.When(
                SetRaceSubRaces(
                    Id=self.RaceId,
                    Subraces=[self.Subrace1Id]
                )
            ),
            self.Then()
        )

        self.Test(
            self.Given(
                RaceCreated(
                    Id=self.RaceId,
                    BaseRaceId=None
                ),
                RaceSubRacesSet(
                    Id=self.RaceId,
                    Subraces=[self.Subrace1Id]
                )
            ),
            self.When(
                SetRaceSubRaces(
                    Id=self.RaceId,
                    Subraces=[self.Subrace2Id]
                )
            ),
            self.Then(
                RaceSubRacesSet(
                    Id=self.RaceId,
                    Subraces=[self.Subrace2Id]
                )
            )
        )

    def test_cannot_set_uncreated_race_sub_races(self):
        self.Test(
            self.Given(),
            self.When(
                SetRaceSubRaces(
                    Id=self.RaceId,
                    Subraces=[self.Subrace1Id]
                )
            ),
            self.ThenFailWith(RaceDoesNotExist)
        )


if __name__ == '__main__':
    unittest.main()
