from .IApplyEvent import IApplyEvent
from .IReadModel import IReadModel
from .IAggregate import IAggregate
from .ICommand import ICommand
from .IEvent import IEvent
from .IEventStore import IEventStore
from .IHandleCommand import IHandleCommand
from .IHandleEvent import IHandleEvent


class MessageDispatcher:
    """
    Event- and Command handler and subscription message dispatcher.
    """

    def __init__(self, eventStore: IEventStore):
        self.commandHandlers = {}
        self.eventHandlers = {}
        self.eventStore = eventStore

    def SendCommand(self, command: ICommand) -> None:
        """
        Publishes the `command` to the scanned `IHandleCommand` command handler class.
        """
        commandType = command.__class__
        if commandType not in self.commandHandlers:
            raise Exception(f"No command handler registered for {commandType}")

        self.commandHandlers[commandType](command)

    def Publish(self, event: IEvent) -> None:
        """
        Publishes the `event` to all registered `IHandleEvent` event handler classes.
        """
        eventType = event.__class__
        if eventType in self.eventHandlers:
            for subscriber in self.eventHandlers[eventType]:
                subscriber(event)

    def AddHandlerOnCommand(self, command_handler: IAggregate, command: ICommand) -> None:
        """
        The `command_handler` is registered to `IHandleCommand.Handle(command)` an unallocated `command`.

        TODO: Consider making it possible to register multiple `IHandleCommand` command handlers on a command,
        and why Edument decided not to this initially.
        """
        if command in self.commandHandlers:
            raise Exception(
                f"Command handler already registered for {command}"
            )

        def handler(command: ICommand) -> None:
            """
            An aggregate of `command_handler` is hydrated for the `command` to `IHandleCommand.Handle(command)`.

            The resulting events are then appended to the `command_handler` aggregate and published to all `IHandleEvent` event handlers.
            """
            aggregate = command_handler.__class__()
            aggregate.ApplyEvents(self.eventStore.LoadEventsForAggregate(command.Id))
            unpublished_events = []
            for commanded_event in aggregate.Handle(command):
                unpublished_events.append(commanded_event)
            if unpublished_events:
                self.eventStore.SaveEvents(aggregate.__class__.__name__, aggregate.EventsLoaded, unpublished_events)
            for event in unpublished_events:
                self.Publish(event)

        self.commandHandlers[command] = handler

    def AddHandlerOnEvent(self, event_handler: IHandleEvent, event: IEvent) -> None:
        """
        `event_handler` is registered to `IHandleEvent.Handle(event)` any events of __class__ `event` 
        """
        if event not in self.eventHandlers:
            self.eventHandlers[event] = []
        self.eventHandlers[event].append(lambda e: event_handler.Handle(e))

    def RegisterHandlersOfInstance(self, instance) -> None:
        """
        `instance` of `IHandleCommand` and/or `IHandleEvent` is scanned and all `Handle()` handlers are registered their respective `@singledispatch` registry key commands and events.

        TODO: `IHandleCommand` command handlers may asof yet only register they handlers on unregistered commands.
        """
        try:
            applyOverload = getattr(instance, 'Apply')
            if applyOverload and callable(applyOverload):
                appliables = instance.Apply.registry.keys()
                revissions = self.eventStore.LoadDomain(instance)
                print('appliables')
                print([appliable.__name__ for appliable in appliables])

                # if len(domain) == 0:

                # readEvents = []
                # instanceIsEventApplier = issubclass(instance.__class__, IApplyEvent)
                # for appliable in appliables:
                #     if issubclass(appliable, IEvent):
                #         if instanceIsEventApplier:
                #             self.AddHandlerOnEvent(instance, handleable)
                #         if instanceIsReadModel:
                #             readEvents.append(handleable.__name__)
                # if instanceIsReadModel:
                #     instance.ReadEvents(self.eventStore.LoadEventsByType(readEvents))
        except Exception as ex:
            print(ex)

        handler = getattr(instance, 'Handle')
        if handler and callable(handler):
            handleables = instance.Handle.registry.keys()
            readEvents = []
            instanceIsReadModel = issubclass(instance.__class__, IReadModel)
            instanceIsCommandHandler = issubclass(instance.__class__, IHandleCommand)
            instanceIsEventHandler = issubclass(instance.__class__, IHandleEvent)
            for handleable in handleables:
                if issubclass(handleable, ICommand) and instanceIsCommandHandler:
                    self.AddHandlerOnCommand(instance, handleable)
                if issubclass(handleable, IEvent):
                    if instanceIsEventHandler:
                        self.AddHandlerOnEvent(instance, handleable)
                    if instanceIsReadModel:
                        readEvents.append(handleable.__name__)
            if instanceIsReadModel:
                instance.ReadEvents(self.eventStore.LoadEventsByType(readEvents))
