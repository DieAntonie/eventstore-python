from dataclasses import dataclass

@dataclass
class OrderedItem:
    MenuNumber: int
    Description: str
    IsDrink: bool
    Price: float