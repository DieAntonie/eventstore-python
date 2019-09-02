from dataclasses import dataclass
import uuid

@dataclass
class TabClosed:
    Id: uuid
    AmountPaid: float
    OrderValue: float
    TipValue: float