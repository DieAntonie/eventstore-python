from abc import ABC, abstractmethod

class IEventStore(ABC):

    @abstractmethod
    def LoadEventsFor(self, id): pass 

    @abstractmethod
    def SaveEventsFor(self, id, eventsLoaded, newEvents): pass 