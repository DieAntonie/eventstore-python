from functools import singledispatch, update_wrapper
from ...Edument_CQRS.Aggregate import Aggregate
from ...Edument_CQRS.IApplyEvent import IApplyEvent
from ...Edument_CQRS.IHandleCommand import IHandleCommand


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


class CharacterAggregate(Aggregate, IHandleCommand, IApplyEvent):
    """
    An instance of the Tab domain object.
    """

    def __init__(self):
        super(CharacterAggregate, self).__init__()

    @methdispatch
    def Handle(self, command):
        """
        Generic `IHandleCommand` overloaded command handler catch all commands that are not registered to be handled.
        """
        raise ValueError(
            f"Aggregate {self.__class__.__name__} does not know how to handle command {command.__class__.__name__}")

    @methdispatch
    def Apply(self, event):
        """
        Generic `IApplyEvent` overloaded event handler catch all events that are not registered to be applied.
        """
        raise ValueError(
            f"Aggregate {self.__class__.__name__} does not know how to apply event {event.__class__.__name__}")