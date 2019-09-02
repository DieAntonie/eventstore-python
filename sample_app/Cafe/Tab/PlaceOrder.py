from dataclasses import dataclass
import uuid

@dataclass
class PlaceOrder:
    Id: uuid 
    Items: []
