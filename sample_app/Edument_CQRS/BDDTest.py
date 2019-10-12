from ..Cafe.Tab.TabAggregate import TabAggregate
from uuid import UUID


class BDDTest():
    def __init__(self, testCase):
        self.testCase = testCase
        self.sut = TabAggregate()

    def Test(self, given, when, then):
        """
        Assert that `given` a premis of applied events that `when` a command is requested, `then` is to be expected.
        """
        then(when(self.ApplyEvents(self.sut, given)))

    def Given(self, *events):
        """
        Premis of `events` that have been applied.
        """
        return events

    def When(self, command):
        """
        Requested `command` to be handled by Aggregate.
        """
        def commandHandler(agg):
            """
            Applies `command` onto `agg`.
            """
            try:
                return self.DispatchCommand(command)
            except Exception as e:
                return e
        return commandHandler

    def Then(self, *expectedTuple):
        """
        Assert that the `expectedTuple` of events corrospond to the result of the applied `BDDTest.When()`.
        """
        expectedEvents = list(expectedTuple)

        def eventHandler(*receivedTuple):
            """
            Handles comparison of expected evenets and recieved events.
            """
            receivedEvents = list(receivedTuple[0])
            if receivedEvents:
                if len(receivedEvents) == len(expectedEvents):
                    for received_event in receivedEvents:
                        if received_event.__class__ in [expected_event.__class__ for expected_event in expectedEvents]:
                            for index, expected_event in enumerate(expectedEvents):
                                if received_event.__class__ == expected_event.__class__:
                                    self.testCase.assertEqual(
                                        self.Serialize(expectedEvents.pop(index)),
                                        self.Serialize(received_event))
                        else:
                            expected_events = [
                                expected_event.__class__.__name__
                                for expected_event in expectedEvents
                            ]
                            self.testCase.fail(f"""
                            Incorrect event in results; expected any of {"; ".join(expected_events)} but got a 
                            {received_event.__class__.__name__}
                            """)
                elif len(receivedEvents) < len(expectedEvents):
                    self.testCase.fail(
                        f"Expected event(s) missing: {self.EventDiff(expectedEvents, receivedEvents)}"
                    )
                else:
                    self.testCase.fail(
                        f"Unexpected event(s) emitted: {self.EventDiff(receivedEvents, expectedEvents)}"
                    )
            else:
                self.testCase.fail(
                    f"Expected events, but got {receivedEvents}"
                )
        return eventHandler

    def EventDiff(self, compare, against):
        """
        Determines the diffirence in events `compare` to that of `against`.
        """
        event_diff = [event.__class__.__name__ for event in compare]
        for to_remove in [event.__class__.__name__ for event in against]:
            event_diff.remove(to_remove)
        return event_diff

    def ThenFailWith(self, expectedException):
        """
        Assert that the `expectedException` is raised as the result of the applied `BDDTest.When()`.
        """
        def exceptionHandler(receivedExceptionTuple):
            """
            Handle the received exception and compare against expected exception.
            """
            with self.testCase.assertRaises(expectedException):
                receivedException = list(receivedExceptionTuple)
                self.testCase.fail(f"""
                Expected exception {expectedException.__class__.__name__}, but got event
                {receivedException.__class__.__name__} result
                """)

        return exceptionHandler

    def DispatchCommand(self, command):
        """
        Apply the `command` onto the aggregate.
        """
        handler = getattr(self.sut, 'Handle')
        if handler is None or not callable(handler):
            return self.CommandHandlerNotDefiendException(f"""
            Aggregate {self.sut.__class__.__name__} does not yet handle commands
            """)
        if handler and callable(handler) and command.__class__ not in self.sut.Handle.registry.keys():
            return self.CommandHandlerNotDefiendException(f"""
            Aggregate {self.sut.__class__.__name__} does not yet handle command {command.__class__.__name__}
            """)
        return handler(command)

    def ApplyEvents(self, agg, events):
        """
        Apply the `events` onto the aggregate.
        """
        agg.ApplyEvents(events)
        return agg

    def Serialize(self, obj):
        """
        Serialize the event objects to comparible json strings.
        """
        import json

        class UUIDEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, UUID):
                    # if the obj is uuid, we simply return the value of uuid
                    return obj.hex
                return obj.__dict__
        return json.dumps(obj.__dict__, cls=UUIDEncoder)

    class CommandHandlerNotDefiendException(Exception):
        pass
