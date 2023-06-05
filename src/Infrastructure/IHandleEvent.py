from abc import ABCMeta, abstractmethod
from .IEvent import IEvent

class IHandleEvent(metaclass=ABCMeta):
    """
    `IEvent` handler interface for read models that can be altered by application of events.
    """
    @abstractmethod
    def Handle(self, event: IEvent) -> None:
        """
        Generic `IHandleEvent` overloaded event handler catch all event that are not registered to be handled.
        """
        raise ValueError(
            f"{self.__class__.__name__} does not know how to handle event {event.__class__.__name__} : {event}")