from dataclasses import dataclass
import uuid


@dataclass
class MarkFoodPrepared:
    """
    Request to mark the specified `MenuNumbers` food as prepared.
    """
    Id: uuid
    MenuNumbers: []
