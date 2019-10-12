from dataclasses import dataclass
import uuid


@dataclass
class DrinksOrdered:
    """
    A fact stating that specified drink `Items: [OrderItems]` have been ordered.
    """
    Id: uuid
    Items: []
