from .IApplyEvent import IApplyEvent
from .ICommand import ICommand
from .IEvent import IEvent
from .IHandleCommand import IHandleCommand
from functools import singledispatch, wraps
from typing import Sequence
import uuid


class Aggregate(IHandleCommand, IApplyEvent):
    """
    Aggregate domain object that is composed of sequential application of events.
    """

    def Overload(func):
        """
        Extended Single-dispatch generic class method decorator.

        Transforms a class method into a generic function, which can have different behaviours depending upon the type of its first argument. The decorated class method acts as the default implementation, and additional implementations can be registered using the `register()` attribute of the generic function.
        """
        dispatcher = singledispatch(func)
        @wraps(func)
        def dispatch_wrapper(*args, **kw):
            """
            Class method dispatch wrapper.
            """
            return dispatcher.dispatch(args[1].__class__)(*args, **kw)
        dispatch_wrapper.register = dispatcher.register
        dispatch_wrapper.registry = dispatcher.registry
        return dispatch_wrapper

    def TargetValidation(func):
        """
        Validate incoming `Command` \ `Event` is addressed to current Aggregate.
        """
        @wraps(func)
        def validate_target_id_match(self, *arguments, **keyword_arguments):
            """
            Validate that `Aggregate.Id` matches incoming `Command.Id` \ `Event.Id` 
            """
            commandId = getattr(arguments[0], 'Id')
            if (type(commandId) is str):
                setattr(arguments[0], 'Id', uuid.UUID(commandId))
            if self.Id is not None and self.Id != getattr(arguments[0], "Id"):
                raise Exception("Jisiis daar's grooooot kak!!!!")

            return func(self, *arguments)

        return validate_target_id_match

    def __init__(self, id=None, eventsLoaded=0):
        self.Id = id
        self.EventsLoaded = eventsLoaded

    @TargetValidation
    @Overload
    def Handle(self, command: ICommand) -> Sequence[IEvent]: super().Handle(command)

    @TargetValidation
    @Overload
    def Apply(self, event: IEvent) -> None: super().Apply(event)

    def ApplyEvents(self, events: Sequence[IEvent]) -> None:
        """
        Sequentially apply the collection of `events`.
        """
        for event in events:
            self.Apply(event)
            self.EventsLoaded += 1
