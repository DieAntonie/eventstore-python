from .IApplyEvent import IApplyEvent
from .IHandleCommand import IHandleCommand
from functools import singledispatch, wraps
import uuid


class Aggregate(IHandleCommand, IApplyEvent):
    """
    Aggregate domain object that is composed of sequential application of events.
    """
    
    def overload(func):
        """
        Extended Single-dispatch generic class method decorator.

        Transforms a class method into a generic function, which can have different behaviours depending upon the type of its first argument. The decorated class method acts as the default implementation, and additional implementations can be registered using the `register()` attribute of the generic function.
        """
        dispatcher = singledispatch(func)
        @wraps(func)
        def wrapper(*args, **kw):
            """
            Generic class method wrapper.
            """
            return dispatcher.dispatch(args[1].__class__)(*args, **kw)
        wrapper.register = dispatcher.register
        wrapper.registry = dispatcher.registry
        return wrapper

    def __init__(self, id=uuid.uuid1(), eventsLoaded=0):
        self.Id = id
        self.EventsLoaded = eventsLoaded

    @overload
    @staticmethod
    def Handle(self, command): super().Handle(command)

    @overload
    @staticmethod
    def Apply(self, event): super().Apply(event)

    def ApplyEvents(self, events):
        """
        Sequentially apply the collection of `events`.
        """
        for event in events:
            getattr(self, 'ApplyOneEvent')(event)

    def ApplyOneEvent(self, event):
        """
        Apply `event` to Aggregate.
        """
        applier = getattr(self, 'Apply')
        if applier is None or not callable(applier):
            raise TypeError(
                f"Aggregate {self.__class__.__name__} must be based of IApplyEvent class"
            )
        applier(event)
        self.EventsLoaded += 1
