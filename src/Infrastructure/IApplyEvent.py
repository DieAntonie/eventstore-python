from abc import ABCMeta, abstractmethod
from .IEvent import IEvent


class IApplyEvent(metaclass=ABCMeta):
    """
    `IEvent` applier interface for aggregates that can be altered by the application of events.
    """
    @abstractmethod
    def Apply(self, event: IEvent) -> None:
        """
        Generic `IApplyEvent` overloaded event applier catch all events that are not registered to be applied.
        """
        raise ValueError(
            f"{self.__class__.__name__} does not know how to apply event {event.__class__.__name__} : {event}")
