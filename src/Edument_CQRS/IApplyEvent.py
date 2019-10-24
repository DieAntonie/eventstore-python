from abc import ABC, abstractmethod


class IApplyEvent(ABC):
    """
    Event Handler interface for `Aggregates` that can be altered by application of events.
    """
    @abstractmethod
    def Apply(self, event): pass
