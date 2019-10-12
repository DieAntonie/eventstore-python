from dataclasses import dataclass
import uuid


@dataclass
class MarkDrinksServed:
    """
    Request to mark the specified `MenuNumbers` drinks as served.
    """
    Id: uuid
    MenuNumbers: []
