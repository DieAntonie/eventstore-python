from dataclasses import dataclass
from ..DiceRoll import DiceRoll
from ..Length import Foot
from ..SizeCategory import SizeCategory
import uuid


@dataclass
class CreateRace:
    """
    Request to assign a `Race` of a certain `Age` and `Alignment` to a `CharacterAggregate`.
    """
    Id: uuid
    BaseRaceId: uuid


@dataclass
class SetRaceDetails:
    """
    Request to assign a `Race` of a certain `Age` and `Alignment` to a `CharacterAggregate`.
    """
    Id: uuid
    Name: str
    Description: str


@dataclass
class SetRaceAbilityScoreIncrease:
    """
    An `ICommand` to assign `AbilityScoreIncrease` to the `RaceAggregte`.
    """
    Id: uuid
    AbilityScoreIncrease: []


@dataclass
class SetRaceAge:
    """
    An `ICommand` to assign the `MaturityAge` and `LifeExpectency` to the `RaceAggregte`.
    """
    Id: uuid
    MaturityAge: int
    LifeExpectency: int


@dataclass
class SetRaceAlignment:
    """
    An `ICommand` to set the `Orthodoxy` and `Morality` of the `RaceAggregte`.
    """
    Id: uuid
    Orthodoxy: int
    Morality: int


@dataclass
class SetRaceSize:
    """
    An `ICommand` to set the `SizeCategory` and `Weight` of the `RaceAggregte`.
    """
    Id: uuid
    SizeCategory: SizeCategory
    BaseHeight: Foot
    HeightModifier: DiceRoll
    BaseWeight: int
    WeightModifier: DiceRoll
