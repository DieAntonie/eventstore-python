from dataclasses import dataclass
import uuid


@dataclass
class CloseTab:
    """
    Request to close the Tab with specified `AmountPaid`.
    """
    Id: uuid
    AmountPaid: float
