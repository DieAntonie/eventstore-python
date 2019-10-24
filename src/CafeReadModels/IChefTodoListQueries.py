from abc import ABC, abstractmethod

class IChefTodoListQueries(ABC):

    @abstractmethod
    def GetTodoList(self): pass 