from abc import ABCMeta, abstractmethod


class IEventStore(metaclass=ABCMeta):
    """
    Event Store interface for loading and storing aggregate event data 
    """
    @abstractmethod
    def LoadEventsFor(self, id): pass

    @abstractmethod
    def SaveEventsFor(self, id, eventsLoaded, newEvents): pass
