from .Commands import (
    CreateRace,
    SetRaceDetails,
    SetRaceAbilityScoreIncrease
)
from .Events import (
    RaceCreated,
    RaceNameSet,
    RaceDescriptionSet,
    RaceAbilityScoreIncreaseSet
)
from .Exceptions import (
    RaceAlreadyCreated,
    RaceCannotBeBasedOnSelf,
    RaceDoesNotExist,
    TooManyOtherAbilityScoreIncreaseTokens,
    InvalidAbilityScoreIncreaseTokenStructure,
    InvalidAbilityScoreIncreaseToken
)
from ..Ability import Ability
from ....Infrastructure.Aggregate import Aggregate
from functools import wraps
from typing import Sequence


class RaceAggregate(Aggregate):
    """
    An instance of the Tab domain object.
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

    @Aggregate.Handle.register(CreateRace)
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

    @Aggregate.Handle.register(SetRaceDetails)
    @RaceMustExist
    def Handle_SetRaceDetails(self, command: SetRaceDetails):
        """
        `OpenTab` command handler that emits a `TabOpened` event upon successfully opening a tab.
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

    @Aggregate.Handle.register(SetRaceAbilityScoreIncrease)
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

    @Aggregate.Apply.register(RaceCreated)
    def Apply_RaceCreated(self, event: RaceCreated):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.Id = event.Id
        self.base_race = event.BaseRaceId

    @Aggregate.Apply.register(RaceNameSet)
    def Apply_RaceNameSet(self, event: RaceNameSet):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.name = event.Name

    @Aggregate.Apply.register(RaceDescriptionSet)
    def Apply_RaceDescriptionSet(self, event: RaceDescriptionSet):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.description = event.Description

    @Aggregate.Apply.register(RaceAbilityScoreIncreaseSet)
    def Apply_RaceAbilityScoreIncreaseSet(self, event: RaceAbilityScoreIncreaseSet):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.ability_score_increase = event.AbilityScoreIncrease
