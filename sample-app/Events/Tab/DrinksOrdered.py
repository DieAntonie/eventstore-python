from dataclasses import dataclass
import uuid

@dataclass
class DrinksOrdered:
    Id: uuid
    Items: []