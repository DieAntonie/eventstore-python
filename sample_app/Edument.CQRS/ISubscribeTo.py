from abc import ABC, abstractmethod

class ISubscribeTo(ABC):

    @abstractmethod
    def Handle(self, event): pass 