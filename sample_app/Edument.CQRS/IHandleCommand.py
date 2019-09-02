from abc import ABC, abstractmethod

class IHandleCommand(ABC):

    @abstractmethod
    def Handle(self, command): pass 