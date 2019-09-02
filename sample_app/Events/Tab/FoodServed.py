from dataclasses import dataclass
import uuid

@dataclass
class FoodServed:
    Id: uuid
    MenuNumbers: []