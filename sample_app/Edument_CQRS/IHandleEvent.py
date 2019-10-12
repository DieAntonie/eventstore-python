from abc import ABC, abstractmethod

class IHandleEvent(ABC):

    @abstractmethod
    def Handle(self, event): pass 