from abc import ABC, abstractmethod


class IEventStore(ABC):
    """
    Event Store interface for loading and storing aggregate event data 
    """
    @abstractmethod
    def LoadEventsFor(self, id): pass

    @abstractmethod
    def SaveEventsFor(self, id, eventsLoaded, newEvents): pass
