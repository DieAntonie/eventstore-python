from abc import ABC, abstractmethod


class IHandleEvent(ABC):
    """
    Event Handler interface for read models that can be altered by application of events.
    """
    @abstractmethod
    def Handle(self, event): pass
