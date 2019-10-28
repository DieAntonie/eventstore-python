from abc import ABCMeta, abstractmethod


class IHandleCommand(metaclass=ABCMeta):
    """
    Command Handler interface for `Aggregates` that can emit some events when handling requested commands.
    """
    @abstractmethod
    def Handle(self, command): pass
