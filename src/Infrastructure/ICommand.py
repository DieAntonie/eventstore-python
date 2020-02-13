from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
import uuid


@dataclass
class ICommand(metaclass=ABCMeta):
    """
    A request.
    """
    Id: uuid
