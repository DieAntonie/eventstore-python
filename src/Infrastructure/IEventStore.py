from .IEvent import IEvent
from abc import ABCMeta, abstractmethod
from typing import Sequence
from uuid import UUID

class IEventStore(metaclass=ABCMeta):
    """
    Event Store interface for loading and storing aggregate event data 
    """
    @abstractmethod
    def LoadEventsByType(self, eventTypes: Sequence[str]) -> Sequence[IEvent]: pass
    
    @abstractmethod
    def LoadEventsForAggregate(self, id: UUID) -> Sequence[IEvent]: pass

    @abstractmethod
    def SaveEvents(self, aggregateType: str, eventsLoaded: int, newEvents: Sequence[IEvent]) -> None: pass

    @abstractmethod
    def LoadDomain(self, domain): pass
