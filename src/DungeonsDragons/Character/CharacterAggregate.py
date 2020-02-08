from functools import singledispatch, update_wrapper
from .Commands.SetRace import SetRace
from .Events.RaceSet import RaceSet
from .Exceptions import RaceAlreadySet
from ...Infrastructure.Aggregate import Aggregate
from ...Infrastructure.IApplyEvent import IApplyEvent
from ...Infrastructure.IHandleCommand import IHandleCommand


def methdispatch(func):
    """
    Extended Single-dispatch generic class method decorator.

    Transforms a class method into a generic function, which can have different behaviours depending upon the type of its first argument. The decorated class method acts as the default implementation, and additional implementations can be registered using the `register()` attribute of the generic function.
    """
    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        """
        Generic class method wrapper.
        """
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    wrapper.register = dispatcher.register
    wrapper.registry = dispatcher.registry
    update_wrapper(wrapper, func)
    return wrapper


class CharacterAggregate(Aggregate, IHandleCommand, IApplyEvent):
    """
    An instance of the Tab domain object.
    """

    def __init__(self):
        super().__init__()
        self.race = None
        self.age = None
        self.alignment = None

    @methdispatch
    def Handle(self, command): super().Handle(command)

    @Handle.register(SetRace)
    def Handle_SetRace(self, command: SetRace):
        """
        `OpenTab` command handler that emits a `TabOpened` event upon successfully opening a tab.
        """
        if self.race is not None:
            raise RaceAlreadySet

        yield RaceSet(
            command.Id,
            command.Race,
            command.Age,
            command.Alignment
        )

    @methdispatch
    def Apply(self, event): super().Apply(event)

    @Apply.register(RaceSet)
    def Apply_RaceSet(self, event: RaceSet):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.race = event.Race
        self.age = event.Age
        self.alignment = event.Alignment
