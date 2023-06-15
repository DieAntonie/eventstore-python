from .Commands import (
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
from .Events import (
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
from .Exceptions import (
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
from ..Ability import Ability
from ....Infrastructure.IAggregate import IAggregate
from functools import wraps
from typing import Sequence


class RaceAggregate(IAggregate):
    """
    An instance of the Race domain object.
    """

    def RaceMustExist(self):
        """
        Test if race is created
        """
        @wraps(self)
        def test_if_race_exists(*arguments, **keyword_arguments):
            if not getattr(arguments[0], "Id"):
                raise RaceDoesNotExist
            return self(*arguments)

        return test_if_race_exists

    def __init__(self):
        super().__init__()
        self.name = None
        self.description = None
        self.base_race = None
        self.ability_score_increase = []
        self.sub_races = []
        self.maturity_age = None
        self.life_expectency = None
        self.orthodoxy = None
        self.morality = None
        self.size_category = None
        self.base_height = None
        self.height_modifier = None
        self.base_weight = None
        self.weight_modifier = None
        self.base_walk_speed = None
        self.languages = []

    @IAggregate.Handle.register(CreateRace)
    def Handle_CreateRace(self, command: CreateRace):
        """
        `CreateRace` command handler that emits a `RaceCreated` event upon successfully creating a race.
        """
        if self.Id:
            raise RaceAlreadyCreated
        if command.Id == command.BaseRaceId:
            raise RaceCannotBeBasedOnSelf

        yield RaceCreated(
            command.Id,
            command.BaseRaceId
        )

    @IAggregate.Handle.register(SetRaceDetails)
    @RaceMustExist
    def Handle_SetRaceDetails(self, command: SetRaceDetails):
        """
        `SetRaceDetails` command handler that emits a `RaceNameSet` event upon successfully opening a tab.
        """
        if command.Name != self.name:
            yield RaceNameSet(
                Id=self.Id,
                Name=command.Name
            )

        if command.Description != self.description:
            yield RaceDescriptionSet(
                Id=self.Id,
                Description=command.Description
            )

    @IAggregate.Handle.register(SetRaceAbilityScoreIncrease)
    @RaceMustExist
    def Handle_SetRaceAbilityScoreIncrease(self, command: SetRaceAbilityScoreIncrease):
        """
        `SetRaceAbilityScoreIncrease` command handler that emits a `RaceAbilityScoreIncreaseSet` upon successful validation.
        """
        self.ValidAbilityScoreIncrease(command.AbilityScoreIncrease)
        if command.AbilityScoreIncrease != self.ability_score_increase:
            yield RaceAbilityScoreIncreaseSet(
                Id=self.Id,
                AbilityScoreIncrease=command.AbilityScoreIncrease
            )

    @IAggregate.Handle.register(SetRaceAge)
    @RaceMustExist
    def Handle_SetRaceAge(self, command: SetRaceAge):
        """
        `SetRaceAge` command handler that emits `RaceMaturityAgeSet` and `RaceLifeExpectancySet` upon successful validation.
        """
        if command.MaturityAge >= command.LifeExpectency:
            raise RaceMaturityAgeExceedsLifeExpectency

        if command.MaturityAge <= 0:
            raise RaceMaturityAgeTooSmall

        if command.MaturityAge != self.maturity_age:
            yield RaceMaturityAgeSet(
                Id=self.Id,
                MaturityAge=command.MaturityAge
            )

        if command.LifeExpectency != self.life_expectency:
            yield RaceLifeExpectancySet(
                Id=self.Id,
                LifeExpectency=command.LifeExpectency
            )

    @IAggregate.Handle.register(SetRaceAlignment)
    @RaceMustExist
    def Handle_SetRaceAlignment(self, command: SetRaceAlignment):
        """
        `SetRaceAlignment` command handler that emits `RaceOrthodoxySet` and `RaceMoralitySet` upon successful validation.
        """
        if not (-1 <= command.Orthodoxy <= 1):
            raise RaceOrthodoxyOutsideAllowedSpectrum

        if not (-1 <= command.Morality <= 1):
            raise RaceMoralityOutsideAllowedSpectrum

        if self.orthodoxy != command.Orthodoxy:
            yield RaceOrthodoxySet(
                Id=self.Id,
                Orthodoxy=command.Orthodoxy
            )

        if self.morality != command.Morality:
            yield RaceMoralitySet(
                Id=self.Id,
                Morality=command.Morality
            )

    @IAggregate.Handle.register(SetRaceSize)
    @RaceMustExist
    def Handle_SetRaceSize(self, command: SetRaceSize):
        """
        `SetRaceSize` command handler that emits `RaceSizeCategorySet`, `RaceBaseHeightSet`, `RaceHeightModifierSet`,
        `RaceBaseWeightSet`, and `RaceWeightModifierSet` upon successful validation.
        """
        if self.size_category != command.SizeCategory:
            yield RaceSizeCategorySet(
                Id=self.Id,
                SizeCategory=command.SizeCategory
            )

        if self.base_height != command.BaseHeight:
            yield RaceBaseHeightSet(
                Id=self.Id,
                BaseHeight=command.BaseHeight
            )

        if self.height_modifier != command.HeightModifier:
            yield RaceHeightModifierSet(
                Id=self.Id,
                HeightModifier=command.HeightModifier
            )

        if self.base_weight != command.BaseWeight:
            yield RaceBaseWeightSet(
                Id=self.Id,
                BaseWeight=command.BaseWeight
            )

        if self.weight_modifier != command.WeightModifier:
            yield RaceWeightModifierSet(
                Id=self.Id,
                WeightModifier=command.WeightModifier
            )

    @IAggregate.Handle.register(SetRaceSpeed)
    @RaceMustExist
    def Handle_SetRaceSpeed(self, command: SetRaceSpeed):
        """
        `SetRaceSpeed` command handler that emits `RaceBaseWalkSpeedSet` upon successful validation.
        """
        if self.base_walk_speed != command.BaseWalkSpeed:
            yield RaceBaseWalkSpeedSet(
                Id=self.Id,
                BaseWalkSpeed=command.BaseWalkSpeed
            )

    @IAggregate.Handle.register(SetRaceLanguages)
    @RaceMustExist
    def Handle_SetRaceLanguages(self, command: SetRaceLanguages):
        """
        `SetRaceSpeed` command handler that emits `RaceLanguagesSet` upon successful validation.
        """
        if self.languages != command.Languages:
            yield RaceLanguagesSet(
                Id=self.Id,
                Languages=command.Languages
            )

    @IAggregate.Handle.register(SetRaceSubRaces)
    @RaceMustExist
    def Handle_SetRaceSubRaces(self, command: SetRaceSubRaces):
        """
        `SetRaceSpeed` command handler that emits `RaceLanguagesSet` upon successful validation.
        """
        if self.sub_races != command.Subraces:
            yield RaceSubRacesSet(
                Id=self.Id,
                Subraces=command.Subraces
            )

    @staticmethod
    def ValidAbilityScoreIncrease(ability_score_increase: Sequence[dict]):
        abilities = {
            Ability.Strength.value: 0,
            Ability.Dexterity.value: 0,
            Ability.Constitution.value: 0,
            Ability.Intelligence.value: 0,
            Ability.Wisdom.value: 0,
            Ability.Charisma.value: 0,
        }
        others = 0
        for token in ability_score_increase:
            if not len(token.keys()) == 1:
                raise InvalidAbilityScoreIncreaseTokenStructure

            token_key = list(token.keys())[0]
            if token_key not in [ability.value for ability in Ability]:
                raise InvalidAbilityScoreIncreaseToken
            elif token_key == Ability.Other.value:
                others += 1
            elif token_key in abilities:
                abilities[token_key] += 1

        if len([ability for ability, count in abilities.items() if count == 0]) <= others:
            raise TooManyOtherAbilityScoreIncreaseTokens

    @IAggregate.Apply.register(RaceCreated)
    def Apply_RaceCreated(self, event: RaceCreated):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.Id = event.Id
        self.base_race = event.BaseRaceId

    @IAggregate.Apply.register(RaceNameSet)
    def Apply_RaceNameSet(self, event: RaceNameSet):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.name = event.Name

    @IAggregate.Apply.register(RaceDescriptionSet)
    def Apply_RaceDescriptionSet(self, event: RaceDescriptionSet):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.description = event.Description

    @IAggregate.Apply.register(RaceAbilityScoreIncreaseSet)
    def Apply_RaceAbilityScoreIncreaseSet(self, event: RaceAbilityScoreIncreaseSet):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.ability_score_increase = event.AbilityScoreIncrease

    @IAggregate.Apply.register(RaceMaturityAgeSet)
    def Apply_RaceMaturityAgeSet(self, event: RaceMaturityAgeSet):
        """
        `RaceMaturityAgeSet` event handler that sets this `RaceAggregate.maturity_age`.
        """
        self.maturity_age = event.MaturityAge

    @IAggregate.Apply.register(RaceLifeExpectancySet)
    def Apply_RaceLifeExpectancySet(self, event: RaceLifeExpectancySet):
        """
        `RaceLifeExpectancySet` event handler that sets this `RaceAggregate.life_expectency`.
        """
        self.life_expectency = event.LifeExpectency

    @IAggregate.Apply.register(RaceOrthodoxySet)
    def Apply_RaceOrthodoxySet(self, event: RaceOrthodoxySet):
        """
        `RaceOrthodoxySet` event handler that sets this `RaceAggregate.orthodoxy`.
        """
        self.orthodoxy = event.Orthodoxy

    @IAggregate.Apply.register(RaceMoralitySet)
    def Apply_RaceMoralitySet(self, event: RaceMoralitySet):
        """
        `RaceMoralitySet` event handler that sets this `RaceAggregate.morality`.
        """
        self.morality = event.Morality

    @IAggregate.Apply.register(RaceSizeCategorySet)
    def Apply_RaceSizeCategorySet(self, event: RaceSizeCategorySet):
        """
        `RaceSizeCategorySet` event handler that sets this `RaceAggregate.size_category`.
        """
        self.size_category = event.SizeCategory

    @IAggregate.Apply.register(RaceBaseHeightSet)
    def Apply_RaceBaseHeightSet(self, event: RaceBaseHeightSet):
        """
        `RaceBaseHeightSet` event handler that sets this `RaceAggregate.base_height`.
        """
        self.base_height = event.BaseHeight

    @IAggregate.Apply.register(RaceHeightModifierSet)
    def Apply_RaceHeightModifierSet(self, event: RaceHeightModifierSet):
        """
        `RaceHeightModifierSet` event handler that sets this `RaceAggregate.height_modifier`.
        """
        self.height_modifier = event.HeightModifier

    @IAggregate.Apply.register(RaceBaseWeightSet)
    def Apply_RaceBaseWeightSet(self, event: RaceBaseWeightSet):
        """
        `RaceBaseWeightSet` event handler that sets this `RaceAggregate.base_weight`.
        """
        self.base_weight = event.BaseWeight

    @IAggregate.Apply.register(RaceWeightModifierSet)
    def Apply_RaceWeightModifierSet(self, event: RaceWeightModifierSet):
        """
        `RaceWeightModifierSet` event handler that sets this `RaceAggregate.weight_modifier`.
        """
        self.weight_modifier = event.WeightModifier

    @IAggregate.Apply.register(RaceBaseWalkSpeedSet)
    def Apply_RaceBaseWalkSpeedSet(self, event: RaceBaseWalkSpeedSet):
        """
        `RaceBaseWalkSpeedSet` event handler that sets this `RaceAggregate.base_walk_speed`.
        """
        self.base_walk_speed = event.BaseWalkSpeed

    @IAggregate.Apply.register(RaceLanguagesSet)
    def Apply_RaceLanguagesSet(self, event: RaceLanguagesSet):
        """
        `RaceLanguagesSet` event handler that sets this `RaceAggregate.base_walk_speed`.
        """
        self.languages = event.Languages

    @IAggregate.Apply.register(RaceSubRacesSet)
    def Apply_RaceSubRacesSet(self, event: RaceSubRacesSet):
        """
        `RaceSubRacesSet` event handler that sets this `RaceAggregate.base_walk_speed`.
        """
        self.sub_races = event.Subraces
