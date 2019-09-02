from ..Cafe.Tab.TabAggregate import TabAggregate
from uuid import UUID

class BDDTest():
    def __init__(self, testCase):
        self.testCase = testCase
        self.sut = TabAggregate()

    def Test(self, given, when, then):
        then(when(self.ApplyEvents(self.sut, given)))

    def Given(self, *events):
        return events

    def When(self, command):
        def commandHandler(agg):
            try:
                return self.DispatchCommand(command)
            except Exception as e:
                return e
        return commandHandler

    def Then(self, *expectedEvents):
        def eventHandler(*receivedEvents):
            if receivedEvents:
                if len(receivedEvents) == len(expectedEvents):
                    for index in range(len(receivedEvents)):
                        if receivedEvents[index].__class__ == expectedEvents[index].__class__:
                            self.testCase.assertEqual(self.Serialize(expectedEvents[index]), self.Serialize(receivedEvents[index]))
                        else:
                            self.testCase.fail(f"Incorrect event in results; expected a {expectedEvents[index].__class__.__name__} but got a {receivedEvents[index]}")
                elif len(receivedEvents) < len(expectedEvents):
                    self.fail(f"Expected event(s) missing: {self.EventDiff(expectedEvents, receivedEvents)}")
                else:
                    self.fail(f"Unexpected event(s) emitted: {self.EventDiff(receivedEvents, expectedEvents)}")
            else:
                self.fail(f"Expected events, but got {receivedEvents}")
        return eventHandler

    def EventDiff(self, compare, against):
        event_diff = [event.__class__.__name__ for event in compare]
        for to_remove in [event.__class__.__name__ for event in against]:
            event_diff.remove(to_remove)
        return event_diff

    def ThenFailWith(self, expectedException):
        def exceptionHandler(receivedException):
            if receivedException is expectedException:
                pass
            elif receivedException is self.CommandHandlerNotDefiendException:
                self.fail(receivedException)
            elif receivedException is Exception:
                self.fail(f"Expected exception {expectedException.__class__.__name__}, but got exception {receivedException.__class__.__name__}")
            else:
                self.fail(f"Expected exception {expectedException.__class__.__name__}, but got event result")
        return exceptionHandler

    def DispatchCommand(self, command):
        handler = getattr(self.sut, 'Handle')
        if handler is None or not callable(handler):
            return self.CommandHandlerNotDefiendException(f"Aggregate {self.sut.__class__.__name__} does not yet handle commands")
        if handler and callable(handler) and command.__class__ not in self.sut.Handle.registry.keys():
            return self.CommandHandlerNotDefiendException(f"Aggregate {self.sut.__class__.__name__} does not yet handle command {command.__class__.__name__}")
        return handler(command)

    def ApplyEvents(self, agg, events):
        agg.ApplyEvents(events)
        return agg

    def Serialize(self, obj):
        def model_to_json(model_obj):
            """
            A function takes in a custom object and returns a dictionary representation of the object.
            This dict representation includes meta data such as the object's module and class names.
            """
            # #  Populate the dictionary with object meta data 
            # json_obj = {
            #     "__class__": model_obj.__class__.__name__,
            #     "__module__": model_obj.__module__
            # }
            # #  Populate the dictionary with object properties
            # json_obj.update(model_obj.__dict__)

            return model_obj.__dict__

        import json
        class UUIDEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, UUID):
                    # if the obj is uuid, we simply return the value of uuid
                    return obj.hex
                return json.JSONEncoder.default(self, obj)

        return json.dumps(obj.__dict__, cls=UUIDEncoder) #, default = model_to_json)

    class CommandHandlerNotDefiendException(Exception) : pass
