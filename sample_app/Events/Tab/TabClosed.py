from dataclasses import dataclass
import uuid


@dataclass
class TabClosed:
    """
    A fact stating that a Tab has been closed with `AmountPaid` for the `OrderValue` leaving `TipValue` for the waiter.
    """
    Id: uuid
    AmountPaid: float
    OrderValue: float
    TipValue: float
