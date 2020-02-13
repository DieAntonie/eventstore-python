from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
import uuid


@dataclass
class IEvent(metaclass=ABCMeta):
    """
    A fact.
    """
    Id: uuid
