from dataclasses import dataclass
import uuid


@dataclass
class FoodServed:
    """
    A fact stating that specified food `Items: [OrderItems]` have been served.
    """
    Id: uuid
    MenuNumbers: []
