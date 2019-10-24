from dataclasses import dataclass
import uuid


@dataclass
class FoodOrdered:
    """
    A fact stating that specified food `Items: [OrderItems]` have been ordered.
    """
    Id: uuid
    Items: []
