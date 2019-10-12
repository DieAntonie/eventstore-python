from dataclasses import dataclass
import uuid


@dataclass
class FoodPrepared:
    """
    A fact stating that specified food `Items: [OrderItems]` have been prepared.
    """
    Id: uuid
    MenuNumbers: []
