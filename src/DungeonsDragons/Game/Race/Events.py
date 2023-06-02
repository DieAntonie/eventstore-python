from dataclasses import dataclass
from ..DiceRoll import DiceRoll
from ..Length import Foot
from ..SizeCategory import SizeCategory
import uuid


@dataclass
class RaceCreated:
    """
    Request to assign a `Race` of a certain `Age` and `Alignment` to a `CharacterAggregate`.
    """
    Id: uuid
    BaseRaceId: str


@dataclass
class RaceNameSet:
    """
    Request to assign a `Race` of a certain `Age` and `Alignment` to a `CharacterAggregate`.
    """
    Id: uuid
    Name: str


@dataclass
class RaceDescriptionSet:
    """
    Request to assign a `Race` of a certain `Age` and `Alignment` to a `CharacterAggregate`.
    """
    Id: uuid
    Description: str


@dataclass
class RaceAbilityScoreIncreaseSet:
    """
    An `IEvent` assigning `AbilityScoreIncrease` to `RaceAggregate`.
    """
    Id: uuid
    AbilityScoreIncrease: []


@dataclass
class RaceMaturityAgeSet:
    """
    An `IEvent` assigning `MaturityAg` to `RaceAggregate`.
    """
    Id: uuid
    MaturityAge: int


@dataclass
class RaceLifeExpectancySet:
    """
    An `IEvent` assigning `LifeExpectency` to `RaceAggregate`.
    """
    Id: uuid
    LifeExpectency: int


@dataclass
class RaceOrthodoxySet:
    """
    An `IEvent` assigning `Orthodoxy` to `RaceAggregate`.
    """
    Id: uuid
    Orthodoxy: int


@dataclass
class RaceMoralitySet:
    """
    An `IEvent` assigning `Morality` to `RaceAggregate`.
    """
    Id: uuid
    Morality: int


@dataclass
class RaceSizeCategorySet:
    """
    An `IEvent` assigning `SizeCategory` to `RaceAggregate`.
    """
    Id: uuid
    SizeCategory: SizeCategory


@dataclass
class RaceBaseWeightSet:
    """
    An `IEvent` assigning `BaseWeight` to `RaceAggregate`.
    """
    Id: uuid
    BaseWeight: int


@dataclass
class RaceWeightModifierSet:
    """
    An `IEvent` assigning `WeightModifier` to `RaceAggregate`.
    """
    Id: uuid
    WeightModifier: DiceRoll


@dataclass
class RaceBaseHeightSet:
    """
    An `IEvent` assigning `BaseHeight` to `RaceAggregate`.
    """
    Id: uuid
    BaseHeight: Foot


@dataclass
class RaceHeightModifierSet:
    """
    An `IEvent` assigning `HeightModifier` to `RaceAggregate`.
    """
    Id: uuid
    HeightModifier: DiceRoll


@dataclass
class RaceBaseWalkSpeedSet:
    """
    An `IEvent` assigning `BaseWalkSpeed` to `RaceAggregate`.
    """
    Id: uuid
    BaseWalkSpeed: Foot
