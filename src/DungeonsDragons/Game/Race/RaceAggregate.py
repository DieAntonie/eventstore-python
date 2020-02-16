from .Commands import (
    CreateRace,
    SetRaceDetails,
    Addsubrace,
    Removesubrace,
    Renamesubrace
)
from .Events import (
    RaceCreated,
    RaceNameSet,
    RaceDescriptionSet,
    subraceAdded,
    subraceRemoved,
    subraceRenamed
)
from .Exceptions import (
    RaceAlreadyCreated,
    RaceCannotBeBasedOnSelf,
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

    def RaceMustExist(self):
        """
        Test if race is created
        """
        @wraps(self)
        def test_if_race_exists(*arguments, **keyword_arguments):
            if not getattr(arguments[0], "Id"):
                raise RaceDoesNotExist
            return self(*arguments)

        return test_if_race_exists

    def __init__(self):
        super().__init__()
        self.name = None
        self.description = None
        self.base_race = None
        self.sub_races = []

    @Aggregate.Handle.register(CreateRace)
    def Handle_CreateRace(self, command: CreateRace):
        """
        `CreateRace` command handler that emits a `RaceCreated` event upon successfully creating a race.
        """
        if self.Id:
            raise RaceAlreadyCreated
        if command.Id == command.BaseRaceId:
            raise RaceCannotBeBasedOnSelf

        yield RaceCreated(
            command.Id,
            command.BaseRaceId
        )

    @Aggregate.Handle.register(SetRaceDetails)
    @RaceMustExist
    def Handle_SetRaceDetails(self, command: SetRaceDetails):
        """
        `OpenTab` command handler that emits a `TabOpened` event upon successfully opening a tab.
        """
        if command.Name != self.name:
            yield RaceNameSet(
                Id=self.Id,
                Name=command.Name
            )

        if command.Description != self.description:
            yield RaceDescriptionSet(
                Id=self.Id,
                Description=command.Description
            )

    @Aggregate.Handle.register(Addsubrace)
    def Handle_Addsubrace(self, command: Addsubrace):
        """
        `OpenTab` command handler that emits a `TabOpened` event upon successfully opening a tab.
        """
        # if command.Name is self.name:
        #     raise subraceNameDoesNotDifferFromBaseRace

        # if command.Name in [sub_race["Name"] for sub_race in self.sub_races]:
        #     raise subraceAlreadyExists

        # yield subraceAdded(
        #     Id=command.Id,
        #     Name=command.Name
        # )

    @Aggregate.Handle.register(Removesubrace)
    def Handle_Removesubrace(self, command: Removesubrace):
        """
        `OpenTab` command handler that emits a `TabOpened` event upon successfully opening a tab.
        """
        # if command.Name not in [sub_race["Name"] for sub_race in self.sub_races]:
        #     raise subraceDoesNotExists

        # yield subraceRemoved(
        #     Id=command.Id,
        #     Name=command.Name
        # )

    @Aggregate.Handle.register(Renamesubrace)
    def Handle_Renamesubrace(self, command: Renamesubrace):
        """
        `OpenTab` command handler that emits a `TabOpened` event upon successfully opening a tab.
        """
        # if command.FromName not in [sub_race["Name"] for sub_race in self.sub_races]:
        #     raise subraceDoesNotExists

        # yield subraceRenamed(
        #     Id=command.Id,
        #     FromName=command.FromName,
        #     ToName=command.ToName
        # )

    @Aggregate.Apply.register(RaceCreated)
    def Apply_RaceCreated(self, event: RaceCreated):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.Id = event.Id
        self.base_race = event.BaseRaceId

    @Aggregate.Apply.register(RaceNameSet)
    def Apply_RaceNameSet(self, event: RaceNameSet):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.name = event.Name

    @Aggregate.Apply.register(RaceDescriptionSet)
    def Apply_RaceDescriptionSet(self, event: RaceDescriptionSet):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        self.description = event.Description

    @Aggregate.Apply.register(subraceAdded)
    def Apply_subraceAdded(self, event: subraceAdded):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        # self.sub_races.append({
        #     "Name": event.Name
        # })

    @Aggregate.Apply.register(subraceRemoved)
    def Apply_subraceRemoved(self, event: subraceRemoved):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        # self.sub_races = [
        #     sub_race for sub_race in self.sub_races if sub_race["Name"] is not event.Name]

    @Aggregate.Apply.register(subraceRenamed)
    def Apply_subraceRenamed(self, event: subraceRenamed):
        """
        `RaceSet` event handler that opens this `TabAggregate`.
        """
        # for sub_race in self.sub_races:
        #     if sub_race["Name"] is event.FromName:
        #         sub_race["Name"] = event.ToName
