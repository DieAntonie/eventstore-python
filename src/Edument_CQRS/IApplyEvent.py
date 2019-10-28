from abc import ABCMeta, abstractmethod


class IApplyEvent(metaclass=ABCMeta):
    """
    Event Handler interface for `Aggregates` that can be altered by application of events.
    """
    @abstractmethod
    def Apply(self, event): pass
