from .IHandleCommand import IHandleCommand
from .IHandleEvent import IHandleEvent


class MessageDispatcher:
    """
    Event- and Command handler and subscription message dispatcher.
    """

    def __init__(self, eventStore):
        self.commandHandlers = {}
        self.eventHandlers = {}
        self.eventStore = eventStore

    def SendCommand(self, command):
        """
        Publishes the `command` to the scanned `IHandleCommand` command handler class.
        """
        commandType = command.__class__
        if commandType not in self.commandHandlers:
            raise Exception(f"No command handler registered for {commandType}")

        self.commandHandlers[commandType](command)

    def Publish(self, event):
        """
        Publishes the `event` to all registered `IHandleEvent` event handler classes.
        """
        eventType = event.__class__
        if eventType in self.eventHandlers:
            for subscriber in self.eventHandlers[eventType]:
                subscriber(event)

    def AddHandlerOnCommand(self, command_handler: IHandleCommand, command):
        """
        The `command_handler` is registered to `IHandleCommand.Handle(command)` an unallocated `command`.

        TODO: Consider making it possible to register multiple `IHandleCommand` command handlers on a command,
        and why Edument decided not to this initially.
        """
        if command in self.commandHandlers:
            raise Exception(
                f"Command handler already registered for {command}"
            )

        def handler(command):
            """
            An aggregate of `command_handler` is hydrated for the `command` to `IHandleCommand.Handle(command)`.

            The resulting events are then appended to the `command_handler` aggregate and published to all `IHandleEvent` event handlers.
            """
            aggregate = command_handler.__class__()
            aggregate.Id = command.Id
            aggregate.ApplyEvents(self.eventStore.LoadEventsFor(aggregate.Id))
            unpublished_events = []
            for commanded_event in aggregate.Handle(command):
                unpublished_events.append(commanded_event)
            if unpublished_events:
                self.eventStore.SaveEventsFor(
                    aggregate.Id, aggregate.__class__.__name__, aggregate.EventsLoaded, unpublished_events
                )
            for event in unpublished_events:
                self.Publish(event)

        self.commandHandlers[command] = handler

    def AddHandlerOnEvent(self, event_handler, event):
        """
        `event_handler` is registered to `IHandleEvent.Handle(event)` any events of __class__ `event` 
        """
        if event not in self.eventHandlers:
            self.eventHandlers[event] = []
        self.eventHandlers[event].append(lambda e: event_handler.Handle(e))

    def RegisterHandlersOfInstance(self, instance):
        """
        `instance` of `IHandleCommand` and/or `IHandleEvent` is scanned and all `Handle()` handlers are registered their respective `@singledispatch` registry key commands and events.

        TODO: `IHandleCommand` command handlers may asof yet only register they handlers on unregistered commands.
        """
        handler = getattr(instance, 'Handle')
        if handler and callable(handler):
            for handleable in instance.Handle.registry.keys():
                if issubclass(instance.__class__, IHandleCommand):
                    self.AddHandlerOnCommand(instance, handleable)
                if issubclass(instance.__class__, IHandleEvent):
                    self.AddHandlerOnEvent(instance, handleable)
