from abc import ABCMeta, abstractmethod


class IHandleEvent(metaclass=ABCMeta):
    """
    Event Handler interface for read models that can be altered by application of events.
    """
    @abstractmethod
    def Handle(self, event): pass
