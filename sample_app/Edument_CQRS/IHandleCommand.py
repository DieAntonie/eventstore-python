from abc import ABC, abstractmethod


class IHandleCommand(ABC):
    """
    Command Handler interface for `Aggregates` that can emit some events when handling requested commands.
    """
    @abstractmethod
    def Handle(self, command): pass
