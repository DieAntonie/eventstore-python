from dataclasses import dataclass
from src.Infrastructure.IEvent import IEvent
from ..DiceRoll import DiceRoll
from ..Language import Language
from ..Length import Foot
from ..SizeCategory import SizeCategory
import uuid


@dataclass
class RaceCreated(IEvent):
    """
    Request to assign a `Race` of a certain `Age` and `Alignment` to a `CharacterAggregate`.
    """
    Id: uuid.UUID
    BaseRaceId: uuid.UUID


@dataclass
class RaceNameSet(IEvent):
    """
    Request to assign a `Race` of a certain `Age` and `Alignment` to a `CharacterAggregate`.
    """
    Id: uuid.UUID
    Name: str


@dataclass
class RaceDescriptionSet(IEvent):
    """
    Request to assign a `Race` of a certain `Age` and `Alignment` to a `CharacterAggregate`.
    """
    Id: uuid.UUID
    Name: str
    Description: str


@dataclass
class RaceAbilityScoreIncreaseSet(IEvent):
    """
    An `IEvent` assigning `AbilityScoreIncrease` to `RaceAggregate`.
    """
    Id: uuid.UUID
    AbilityScoreIncrease: list[dict[str, int]]


@dataclass
class RaceMaturityAgeSet(IEvent):
    """
    An `IEvent` assigning `MaturityAg` to `RaceAggregate`.
    """
    Id: uuid.UUID
    MaturityAge: int


@dataclass
class RaceLifeExpectancySet(IEvent):
    """
    An `IEvent` assigning `LifeExpectency` to `RaceAggregate`.
    """
    Id: uuid.UUID
    LifeExpectency: int


@dataclass
class RaceOrthodoxySet(IEvent):
    """
    An `IEvent` assigning `Orthodoxy` to `RaceAggregate`.
    """
    Id: uuid.UUID
    Orthodoxy: int


@dataclass
class RaceMoralitySet(IEvent):
    """
    An `IEvent` assigning `Morality` to `RaceAggregate`.
    """
    Id: uuid.UUID
    Morality: int


@dataclass
class RaceSizeCategorySet(IEvent):
    """
    An `IEvent` assigning `SizeCategory` to `RaceAggregate`.
    """
    Id: uuid.UUID
    SizeCategory: SizeCategory


@dataclass
class RaceBaseWeightSet(IEvent):
    """
    An `IEvent` assigning `BaseWeight` to `RaceAggregate`.
    """
    Id: uuid.UUID
    BaseWeight: int


@dataclass
class RaceWeightModifierSet(IEvent):
    """
    An `IEvent` assigning `WeightModifier` to `RaceAggregate`.
    """
    Id: uuid.UUID
    WeightModifier: DiceRoll


@dataclass
class RaceBaseHeightSet(IEvent):
    """
    An `IEvent` assigning `BaseHeight` to `RaceAggregate`.
    """
    Id: uuid.UUID
    BaseHeight: Foot


@dataclass
class RaceHeightModifierSet(IEvent):
    """
    An `IEvent` assigning `HeightModifier` to `RaceAggregate`.
    """
    Id: uuid.UUID
    HeightModifier: DiceRoll


@dataclass
class RaceBaseWalkSpeedSet(IEvent):
    """
    An `IEvent` assigning `BaseWalkSpeed` to `RaceAggregate`.
    """
    Id: uuid.UUID
    BaseWalkSpeed: Foot


@dataclass
class RaceLanguagesSet(IEvent):
    """
    An `IEvent` assigning `Languages` to `RaceAggregate`.
    """
    Id: uuid.UUID
    Languages: list[Language]


@dataclass
class RaceSubRacesSet(IEvent):
    """
    An `IEvent` assigning `Subraces` to `RaceAggregate`.
    """
    Id: uuid.UUID
    Subraces: list[uuid.UUID]


@dataclass
class RaceUnhandledSet(IEvent):
    """
    An `IEvent` assigning `Languages` to `RaceAggregate`.
    """
    Id: uuid.UUID
