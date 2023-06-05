from .IHandleEvent import IHandleEvent
from .IEvent import IEvent
from .Overloadable import Overloadable

class IReadModel(IHandleEvent):
    @Overloadable
    def Handle(self, event: IEvent) -> None: super().Handle(event)
