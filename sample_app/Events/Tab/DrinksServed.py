from dataclasses import dataclass
import uuid


@dataclass
class DrinksServed:
    """
    A fact stating that specified drink `Items: [OrderItems]` have been served.
    """
    Id: uuid
    MenuNumbers: []
