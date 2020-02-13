from .Commands import (
    CreateRace,
    ChangeRaceName,
    Addsubrace,
    Removesubrace,
    Renamesubrace
)
from .Events import (
    RaceCreated,
    RaceNameChanged,
    subraceAdded,
    subraceRemoved,
    subraceRenamed
)
from .Exceptions import (
    RaceAlreadyCreated,
    RaceDoesNotExist,
    RaceNameDoesNotDiffer,
    subraceNameDoesNotDifferFromBaseRace,
    subraceAlreadyExists,
    subraceDoesNotExists
)
from ....Infrastructure.Aggregate import Aggregate
from functools import wraps


class RaceAggregate(Aggregate):
    """
    An instance of the Tab domain object.
    """

    def __init__(self):
        super().__init__()
        self.created = False
        self.name = None
        self.sub_races = []

    def RaceMustExist(handler):
        @wraps(handler)
        def test_if_race_exists(self, *arguments, **keyword_arguments):
            if not getattr(self, "created"):
                raise RaceDoesNotExist

            return handler(self, *arguments)

        return test_if_race_exists

    @Aggregate.Handle.register(CreateRace)
    def Handle_CreateRace(self, command: CreateRace):
        """
        `OpenTab` command handler that emits a `TabOpened` event upon successfully opening a tab.
        """
        if self.created:
            raise RaceAlreadyCreated

        yield RaceCreated(
            command.Id,
            command.Name
        )

    @Aggregate.Handle.register(ChangeRaceName)
    @RaceMustExist
    def Handle_ChangeRaceName(self, command: ChangeRaceName):
        """
        `OpenTab` command handler that emits a `TabOpened` event upon successfully opening a tab.
        """

        if command.Name is self.name:
            raise RaceNameDoesNotDiffer

        yield RaceNameChanged(
            Id=command.Id,
            FromName=self.name,
            ToName=command.Name
        )

    @Aggregate.Handle.register(Addsubrace)
    @RaceMustExist
    def Handle_Addsubrace(self, command: Addsubrace):
        """
        `OpenTab` command handler that emits a `TabOpened` event upon successfully opening a tab.
        """
        if command.Name is self.name:
            raise subraceNameDoesNotDifferFromBaseRace

        if command.Name in [sub_race["Name"] for sub_race in self.sub_races]:
            raise subraceAlreadyExists

        yield subraceAdded(
            Id=command.Id,
            Name=command.Name
        )

    @Aggregate.Handle.register(Removesubrace)
    @RaceMustExist
    def Handle_Removesubrace(self, command: Removesubrace):
        """
        `OpenTab` command handler that emits a `TabOpened` event upon successfully opening a tab.
        """
        if command.Name not in [sub_race["Name"] for sub_race in self.sub_races]:
            raise subraceDoesNotExists

        yield subraceRemoved(
            Id=command.Id,
            Name=command.Name
        )

    @Aggregate.Handle.register(Renamesubrace)
    @RaceMustExist
    def Handle_Renamesubrace(self, command: Renamesubrace):
        """
        `OpenTab` command handler that emits a `TabOpened` event upon successfully opening a tab.
        """
        if command.FromName not in [sub_race["Name"] for sub_race in self.sub_races]:
            raise subraceDoesNotExists

        yield subraceRenamed(
            Id=command.Id,
            FromName=command.FromName,
            ToName=command.ToName
        )

    @Aggregate.Apply.register(RaceCreated)
    def Apply_RaceCreated(self, event: RaceCreated):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.created = True
        self.name = event.Name

    @Aggregate.Apply.register(RaceNameChanged)
    def Apply_RaceNameChanged(self, event: RaceNameChanged):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.name = event.ToName

    @Aggregate.Apply.register(subraceAdded)
    def Apply_subraceAdded(self, event: subraceAdded):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.sub_races.append({
            "Name": event.Name
        })

    @Aggregate.Apply.register(subraceRemoved)
    def Apply_subraceRemoved(self, event: subraceRemoved):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.sub_races = [
            sub_race for sub_race in self.sub_races if sub_race["Name"] is not event.Name]

    @Aggregate.Apply.register(subraceRenamed)
    def Apply_subraceRenamed(self, event: subraceRenamed):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        for sub_race in self.sub_races:
            if sub_race["Name"] is event.FromName:
                sub_race["Name"] = event.ToName
