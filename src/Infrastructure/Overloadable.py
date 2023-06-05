from functools import singledispatch, wraps

def Overloadable(func):
    """
    Extended Single-dispatch generic class method decorator.

    Transforms a class method into a generic function, which can have different behaviours depending upon the type of its first argument. The decorated class method acts as the default implementation, and additional implementations can be registered using the `register()` attribute of the generic function.
    """
    dispatcher = singledispatch(func)
    @wraps(func)
    def dispatch_wrapper(*args, **kw):
        """
        Class method dispatch wrapper.
        """
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    dispatch_wrapper.register = dispatcher.register
    dispatch_wrapper.registry = dispatcher.registry
    return dispatch_wrapper
