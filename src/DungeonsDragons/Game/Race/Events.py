from dataclasses import dataclass
from ..DiceRoll import DiceRoll
from ..Language import Language
from ..Length import Foot
from ..SizeCategory import SizeCategory
import uuid


@dataclass
class RaceCreated:
    """
    Request to assign a `Race` of a certain `Age` and `Alignment` to a `CharacterAggregate`.
    """
    Id: uuid.UUID
    BaseRaceId: str


@dataclass
class RaceNameSet:
    """
    Request to assign a `Race` of a certain `Age` and `Alignment` to a `CharacterAggregate`.
    """
    Id: uuid.UUID
    Name: str


@dataclass
class RaceDescriptionSet:
    """
    Request to assign a `Race` of a certain `Age` and `Alignment` to a `CharacterAggregate`.
    """
    Id: uuid.UUID
    Description: str


@dataclass
class RaceAbilityScoreIncreaseSet:
    """
    An `IEvent` assigning `AbilityScoreIncrease` to `RaceAggregate`.
    """
    Id: uuid.UUID
    AbilityScoreIncrease: list[dict[str, int]]


@dataclass
class RaceMaturityAgeSet:
    """
    An `IEvent` assigning `MaturityAg` to `RaceAggregate`.
    """
    Id: uuid.UUID
    MaturityAge: int


@dataclass
class RaceLifeExpectancySet:
    """
    An `IEvent` assigning `LifeExpectency` to `RaceAggregate`.
    """
    Id: uuid.UUID
    LifeExpectency: int


@dataclass
class RaceOrthodoxySet:
    """
    An `IEvent` assigning `Orthodoxy` to `RaceAggregate`.
    """
    Id: uuid.UUID
    Orthodoxy: int


@dataclass
class RaceMoralitySet:
    """
    An `IEvent` assigning `Morality` to `RaceAggregate`.
    """
    Id: uuid.UUID
    Morality: int


@dataclass
class RaceSizeCategorySet:
    """
    An `IEvent` assigning `SizeCategory` to `RaceAggregate`.
    """
    Id: uuid.UUID
    SizeCategory: SizeCategory


@dataclass
class RaceBaseWeightSet:
    """
    An `IEvent` assigning `BaseWeight` to `RaceAggregate`.
    """
    Id: uuid.UUID
    BaseWeight: int


@dataclass
class RaceWeightModifierSet:
    """
    An `IEvent` assigning `WeightModifier` to `RaceAggregate`.
    """
    Id: uuid.UUID
    WeightModifier: DiceRoll


@dataclass
class RaceBaseHeightSet:
    """
    An `IEvent` assigning `BaseHeight` to `RaceAggregate`.
    """
    Id: uuid.UUID
    BaseHeight: Foot


@dataclass
class RaceHeightModifierSet:
    """
    An `IEvent` assigning `HeightModifier` to `RaceAggregate`.
    """
    Id: uuid.UUID
    HeightModifier: DiceRoll


@dataclass
class RaceBaseWalkSpeedSet:
    """
    An `IEvent` assigning `BaseWalkSpeed` to `RaceAggregate`.
    """
    Id: uuid.UUID
    BaseWalkSpeed: Foot


@dataclass
class RaceLanguagesSet:
    """
    An `IEvent` assigning `Languages` to `RaceAggregate`.
    """
    Id: uuid.UUID
    Languages: list[Language]


@dataclass
class RaceSubRacesSet:
    """
    An `IEvent` assigning `Subraces` to `RaceAggregate`.
    """
    Id: uuid.UUID
    Subraces: list[uuid.UUID]
