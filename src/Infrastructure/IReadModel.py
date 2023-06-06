from .IHandleEvent import IHandleEvent
from .IEvent import IEvent
from .Overloadable import Overloadable
from typing import Sequence

class IReadModel(IHandleEvent):
    """
    `IEvent` reader interface for read models that can be altered by application of events.
    """
    @Overloadable
    def Handle(self, event: IEvent) -> None: super().Handle(event)

    def ReadEvents(self, events: Sequence[IEvent]) -> None:
        for event in events:
            self.Handle(event)
