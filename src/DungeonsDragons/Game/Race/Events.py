from dataclasses import dataclass
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
