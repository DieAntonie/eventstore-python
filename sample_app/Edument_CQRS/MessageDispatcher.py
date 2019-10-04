from .IHandleCommand import IHandleCommand
from .ISubscribeTo import ISubscribeTo

class MessageDispatcher:
    def __init__(self, eventStore):
        self.commandHandlers = {}
        self.eventSubscribers = {}
        self.eventStore = eventStore

    def SendCommand(self, command):
        commandType = command.__class__.__name__
        if commandType in self.commandHandlers:
            self.commandHandlers[commandType](command)
        else:
            raise Exception(f"No command handler registered for {commandType}")

    def PublishEvent(self, event):
        eventType = event.__class__.__name__
        if eventType in self.eventSubscribers:
            for subscriber in self.eventSubscribers[eventType]:
                subscriber(event)

    def AddHandlerFor(self, command, aggregate):
        if command in self.commandHandlers:
            raise Exception(f"Command handler already registered for {command}")

        def handler(command):
            # Create an empty aggregate.
            agg = aggregate.__class__()
            # Load the aggregate with events.
            agg.Id = command.Id
            agg.ApplyEvents(self.eventStore.LoadEventsFor(agg.Id))
            # With everything set up, we invoke the command handler, collecting the
            # events that it produces.
            resultEvents = []
            for event in agg.Handle(command):
                resultEvents.append(event)
            # Store the events in the event store.
            if resultEvents:
                self.eventStore.SaveEventsFor(agg.Id, agg.EventsLoaded, resultEvents)
            # Publish them to all subscribers.
            for event in resultEvents:
                self.PublishEvent(event)
        
        self.commandHandlers[command] = handler


    def AddSubscriberFor(self, event, subscriber):
        if event not in self.eventSubscribers:
            self.eventSubscribers[event] = []
        self.eventSubscribers[event].append( lambda e : subscriber.Handle(e))

    def ScanInstance(self, instance):
        handler = getattr(instance, 'Handle')
        if handler and callable(handler):
            for argType in instance.Handle.registry.keys():
                # Scan for and register handlers.
                if issubclass(instance.__class__ , IHandleCommand):
                    self.AddHandlerFor(argType, instance)
                # Scan for and register subscribers.
                if issubclass(instance.__class__, ISubscribeTo):
                    self.AddSubscriberFor(argType, instance)
