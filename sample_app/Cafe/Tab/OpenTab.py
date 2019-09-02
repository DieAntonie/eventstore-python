from dataclasses import dataclass
import uuid

@dataclass
class OpenTab:
    """
    Open tab command
    """
    Id: uuid
    TableNumber: int
    Waiter: str
