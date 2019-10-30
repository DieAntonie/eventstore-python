from functools import singledispatch, update_wrapper
from ...Infrastructure.Aggregate import Aggregate
from ...Infrastructure.IApplyEvent import IApplyEvent
from ...Infrastructure.IHandleCommand import IHandleCommand

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


class EnvironmentAggregate(Aggregate, IHandleCommand, IApplyEvent):
    """
    An instance of the Tab domain object.
    """

    def __init__(self):
        super().__init__()