from abc import ABCMeta, abstractmethod
from .IEvent import IEvent


class IApplyEvent(metaclass=ABCMeta):
    """
    Event Handler interface for `Aggregates` that can be altered by application of events.
    """
    @abstractmethod
    def Apply(self, event: IEvent) -> None:
        """
        Generic `IApplyEvent` overloaded event handler catch all events that are not registered to be applied.
        """
        raise ValueError(
            f"{self.__class__.__name__} does not know how to apply event {event.__class__.__name__}")
