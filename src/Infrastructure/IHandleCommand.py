from abc import ABCMeta, abstractmethod
from .ICommand import ICommand
from .IEvent import IEvent
from typing import Sequence


class IHandleCommand(metaclass=ABCMeta):
    """
    Command Handler interface for `Aggregates` that can emit some events when handling requested commands.
    """
    @abstractmethod
    def Handle(self, command: ICommand) -> Sequence[IEvent]:
        """
        Generic `IHandleCommand` overloaded command handler catch all commands that are not registered to be handled.
        """
        raise ValueError(
            f"{self.__class__.__name__} does not know how to handle command {command.__class__.__name__} : {command}")