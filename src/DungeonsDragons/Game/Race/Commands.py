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
