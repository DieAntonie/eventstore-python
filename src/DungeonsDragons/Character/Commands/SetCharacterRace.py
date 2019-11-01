from dataclasses import dataclass
from ...Game.Race import Race
from ...Game.Alignment import Alignment
import uuid


@dataclass
class SetCharacterRace:
    """
    Request to assign a `Race` of a certain `Age` and `Alignment` to a `CharacterAggregate`.
    """
    Id: uuid
    Race: Race
    Age: int
    Alignment: Alignment
