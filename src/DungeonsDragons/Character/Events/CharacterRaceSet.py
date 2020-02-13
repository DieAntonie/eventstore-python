from dataclasses import dataclass
from ...Game.Race import Race
from ...Game.Alignment import Alignment
import uuid


@dataclass
class CharacterRaceSet:
    """
    A fact stating that a `CharacterAggregate` has been assigned a `Race` of a certain `Age` and `Alignment`.
    """
    Id: uuid
    Race: Race
    Age: int
    Alignment: Alignment
