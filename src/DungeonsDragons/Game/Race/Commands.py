from dataclasses import dataclass
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
