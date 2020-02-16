from .Commands import (
    CreateRace,
    SetRaceDetails
)
from .Events import (
    RaceCreated,
    RaceNameSet,
    RaceDescriptionSet
)
from .Exceptions import (
    RaceAlreadyCreated,
    RaceCannotBeBasedOnSelf,
    RaceDoesNotExist
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
