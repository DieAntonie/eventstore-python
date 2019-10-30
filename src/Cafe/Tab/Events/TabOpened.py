from dataclasses import dataclass
import uuid


@dataclass
class TabOpened:
    """
    A fact stating that a Tab has been opened for `TableNumber` by `Waiter`.
    """
    Id: uuid
    TableNumber: int
    Waiter: str
