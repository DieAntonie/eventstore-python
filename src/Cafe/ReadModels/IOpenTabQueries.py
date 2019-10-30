from abc import ABC, abstractmethod

class IOpenTabQueries(ABC):

    @abstractmethod
    def ActiveTableNumbers(self): pass 

    @abstractmethod
    def InvoiceForTable(self, table): pass 

    @abstractmethod
    def TabIdForTable(self, table): pass 

    @abstractmethod
    def TabForTable(self, table): pass 

    @abstractmethod
    def TodoListForWaiter(self, waiter): pass 