import uuid

class Aggregate:
    def __init__(self, id = uuid.uuid1(), eventsLoaded = 0):
        self.Id = id
        self.EventsLoaded = eventsLoaded

    def ApplyEvents(self, events):
        for event in events:
            getattr(self, 'ApplyOneEvent')(event)
    
    def ApplyOneEvent(self, event):
        applier = getattr(self, 'Apply')
        if applier is None or not callable(applier):
            raise TypeError(f"Aggregate {self.__class__.__name__} must be based of IApplyEvent class")
        applier(event)
        self.EventsLoaded += 1
