from dataclasses import dataclass
import uuid

@dataclass
class TabOpened:
    Id: uuid
    TableNumber: int
    Waiter: str