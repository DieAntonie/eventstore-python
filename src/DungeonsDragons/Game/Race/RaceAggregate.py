from functools import singledispatch, update_wrapper
from .Commands import (
    CreateCharacterRace,
    ChangeCharacterRaceName,
    AddCharacterSubrace,
    RemoveCharacterSubrace,
    RenameCharacterSubrace
)
from .Events import (
    CharacterRaceCreated,
    CharacterRaceNameChanged,
    CharacterSubraceAdded,
    CharacterSubraceRemoved,
    CharacterSubraceRenamed
)
from .Exceptions import (
    CharacterRaceAlreadyCreated,
    CharacterRaceDoesNotExist,
    CharacterRaceNameDoesNotDiffer,
    CharacterSubraceNameDoesNotDifferFromBaseRace,
    CharacterSubraceAlreadyExists,
    CharacterSubraceDoesNotExists
)
from ....Infrastructure.Aggregate import Aggregate
from ....Infrastructure.IApplyEvent import IApplyEvent
from ....Infrastructure.IHandleCommand import IHandleCommand


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


class RaceAggregate(Aggregate, IHandleCommand, IApplyEvent):
    """
    An instance of the Tab domain object.
    """

    def __init__(self):
        super().__init__()
        self.created = False
        self.name = None
        self.sub_races = []

    @methdispatch
    def Handle(self, command):
        """
        Generic `IHandleCommand` overloaded command handler catch all commands that are not registered to be handled.
        """
        raise ValueError(
            f"Aggregate {self.__class__.__name__} does not know how to handle command {command.__class__.__name__}")

    @Handle.register(CreateCharacterRace)
    def Handle_CreateCharacterRace(self, command: CreateCharacterRace):
        """
        `OpenTab` command handler that emits a `TabOpened` event upon successfully opening a tab.
        """
        if self.created:
            raise CharacterRaceAlreadyCreated

        yield CharacterRaceCreated(
            command.Id,
            command.Name
        )

    @Handle.register(ChangeCharacterRaceName)
    def Handle_ChangeCharacterRaceName(self, command: ChangeCharacterRaceName):
        """
        `OpenTab` command handler that emits a `TabOpened` event upon successfully opening a tab.
        """
        if not self.created:
            raise CharacterRaceDoesNotExist

        if command.Name is self.name:
            raise CharacterRaceNameDoesNotDiffer

        yield CharacterRaceNameChanged(
            Id=command.Id,
            FromName=self.name,
            ToName=command.Name
        )

    @Handle.register(AddCharacterSubrace)
    def Handle_AddCharacterSubrace(self, command: AddCharacterSubrace):
        """
        `OpenTab` command handler that emits a `TabOpened` event upon successfully opening a tab.
        """
        if not self.created:
            raise CharacterRaceDoesNotExist

        if command.Name is self.name:
            raise CharacterSubraceNameDoesNotDifferFromBaseRace

        if command.Name in [sub_race["Name"] for sub_race in self.sub_races]:
            raise CharacterSubraceAlreadyExists

        yield CharacterSubraceAdded(
            Id=command.Id,
            Name=command.Name
        )

    @Handle.register(RemoveCharacterSubrace)
    def Handle_RemoveCharacterSubrace(self, command: RemoveCharacterSubrace):
        """
        `OpenTab` command handler that emits a `TabOpened` event upon successfully opening a tab.
        """
        if not self.created:
            raise CharacterRaceDoesNotExist

        if command.Name not in [sub_race["Name"] for sub_race in self.sub_races]:
            raise CharacterSubraceDoesNotExists

        yield CharacterSubraceRemoved(
            Id=command.Id,
            Name=command.Name
        )

    @Handle.register(RenameCharacterSubrace)
    def Handle_RenameCharacterSubrace(self, command: RenameCharacterSubrace):
        """
        `OpenTab` command handler that emits a `TabOpened` event upon successfully opening a tab.
        """
        if not self.created:
            raise CharacterRaceDoesNotExist

        if command.FromName not in [sub_race["Name"] for sub_race in self.sub_races]:
            raise CharacterSubraceDoesNotExists

        yield CharacterSubraceRenamed(
            Id=command.Id,
            FromName=command.FromName,
            ToName=command.ToName
        )

    @methdispatch
    def Apply(self, event):
        """
        Generic `IApplyEvent` overloaded event handler catch all events that are not registered to be applied.
        """
        raise ValueError(
            f"Aggregate {self.__class__.__name__} does not know how to apply event {event.__class__.__name__}")

    @Apply.register(CharacterRaceCreated)
    def Apply_CharacterRaceCreated(self, event: CharacterRaceCreated):
        """
        `CharacterRaceSet` event handler that opens this `TabAggregate`.
        """
        self.created = True
        self.name = event.Name

    @Apply.register(CharacterRaceNameChanged)
    def Apply_CharacterRaceNameChanged(self, event: CharacterRaceNameChanged):
        """
        `CharacterRaceSet` event handler that opens this `TabAggregate`.
        """
        self.name = event.ToName

    @Apply.register(CharacterSubraceAdded)
    def Apply_CharacterSubraceAdded(self, event: CharacterSubraceAdded):
        """
        `CharacterRaceSet` event handler that opens this `TabAggregate`.
        """
        self.sub_races.append({
            "Name": event.Name
        })

    @Apply.register(CharacterSubraceRemoved)
    def Apply_CharacterSubraceRemoved(self, event: CharacterSubraceRemoved):
        """
        `CharacterRaceSet` event handler that opens this `TabAggregate`.
        """
        self.sub_races = [sub_race for sub_race in self.sub_races if sub_race["Name"] is not event.Name]

    @Apply.register(CharacterSubraceRenamed)
    def Apply_CharacterSubraceRenamed(self, event: CharacterSubraceRenamed):
        """
        `CharacterRaceSet` event handler that opens this `TabAggregate`.
        """
        for sub_race in self.sub_races:
            if sub_race["Name"] is event.FromName:
                sub_race["Name"] = event.ToName
