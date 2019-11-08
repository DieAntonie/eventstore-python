from dataclasses import dataclass
import uuid


@dataclass
class CharacterRaceCreated:
    """
    Request to assign a `Race` of a certain `Age` and `Alignment` to a `CharacterAggregate`.
    """
    Id: uuid
    Name: str


@dataclass
class CharacterRaceNameChanged:
    """
    Request to assign a `Race` of a certain `Age` and `Alignment` to a `CharacterAggregate`.
    """
    Id: uuid
    FromName: str
    ToName: str
