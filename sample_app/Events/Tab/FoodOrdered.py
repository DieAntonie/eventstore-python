from dataclasses import dataclass
import uuid

@dataclass
class FoodOrdered:
    Id: uuid
    Items: []