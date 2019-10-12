from dataclasses import dataclass
import uuid


@dataclass
class MarkFoodServed:
    """
    Request to mark the specified `MenuNumbers` food as served.
    """
    Id: uuid
    MenuNumbers: []
