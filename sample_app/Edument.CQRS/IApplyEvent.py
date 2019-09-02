from abc import ABC, abstractmethod

class IApplyEvent(ABC):

    @abstractmethod
    def Apply(self, event): pass 