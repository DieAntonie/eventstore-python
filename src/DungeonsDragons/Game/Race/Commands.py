from dataclasses import dataclass
from typing import Optional
from ....Infrastructure.ICommand import ICommand
from ..DiceRoll import DiceRoll
from ..Length import Foot
from ..SizeCategory import SizeCategory
from ..Language import Language
import uuid


@dataclass
class CreateRace(ICommand):
    """
    Request to assign a `Race` of a certain `Age` and `Alignment` to a `CharacterAggregate`.
    """
    Id: uuid.UUID
    BaseRaceId: Optional[uuid.UUID] = None


@dataclass
class SetRaceDetails(ICommand):
    """
    Request to assign a `Race` of a certain `Age` and `Alignment` to a `CharacterAggregate`.
    """
    Id: uuid.UUID
    Name: str
    Description: str


@dataclass
class SetRaceAbilityScoreIncrease(ICommand):
    """
    An `ICommand` to assign `AbilityScoreIncrease` to the `RaceAggregte`.
    """
    Id: uuid.UUID
    AbilityScoreIncrease: list[dict[str, int]]


@dataclass
class SetRaceAge(ICommand):
    """
    An `ICommand` to assign the `MaturityAge` and `LifeExpectency` to the `RaceAggregte`.
    """
    Id: uuid.UUID
    MaturityAge: int
    LifeExpectency: int


@dataclass
class SetRaceAlignment(ICommand):
    """
    An `ICommand` to set the `Orthodoxy` and `Morality` of the `RaceAggregte`.
    """
    Id: uuid.UUID
    Orthodoxy: int
    Morality: int


@dataclass
class SetRaceSize(ICommand):
    """
    An `ICommand` to set the `SizeCategory`, `BaseHeight`, `HeightModifier`, `BaseWeight`,
    and `WeightModifier` of the `RaceAggregte`.
    """
    Id: uuid.UUID
    SizeCategory: SizeCategory
    BaseHeight: Foot
    HeightModifier: DiceRoll
    BaseWeight: int
    WeightModifier: DiceRoll


@dataclass
class SetRaceSpeed(ICommand):
    """
    An `ICommand` to set the `BaseWalkSpeed` of the `RaceAggregte`.
    """
    Id: uuid.UUID
    BaseWalkSpeed: Foot


@dataclass
class SetRaceLanguages(ICommand):
    """
    An `ICommand` to set the `Languages` of the `RaceAggregte`.
    """
    Id: uuid.UUID
    Languages: list[Language]


@dataclass
class SetRaceSubRaces(ICommand):
    """
    An `ICommand` to set the `Subraces` of the `RaceAggregte`.
    """
    Id: uuid.UUID
    Subraces: list[uuid.UUID]
