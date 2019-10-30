from dataclasses import dataclass
import uuid


@dataclass
class PlaceOrder:
    """
    Request to place and order with the specified `Items : [OrderItem]`.
    """
    Id: uuid
    Items: []
