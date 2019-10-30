from dataclasses import dataclass
import uuid


@dataclass
class OpenTab:
    """
    Request to open a Tab at the specified `TableNumber` for the specified `Waiter`.
    """
    Id: uuid
    TableNumber: int
    Waiter: str
