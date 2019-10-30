from dataclasses import dataclass
from functools import singledispatch, update_wrapper
from .IOpenTabQueries import IOpenTabQueries
from ..Infrastructure.IHandleEvent import IHandleEvent
from ..Events.Tab.DrinksOrdered import DrinksOrdered
from ..Events.Tab.DrinksServed import DrinksServed
from ..Events.Tab.FoodOrdered import FoodOrdered
from ..Events.Tab.FoodPrepared import FoodPrepared
from ..Events.Tab.FoodServed import FoodServed
from ..Events.Tab.TabClosed import TabClosed
from ..Events.Tab.TabOpened import TabOpened
import uuid

def methdispatch(func):
    dispatcher = singledispatch(func)
    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    wrapper.register = dispatcher.register
    wrapper.registry = dispatcher.registry
    update_wrapper(wrapper, func)
    return wrapper

class OpenTabs(IOpenTabQueries, IHandleEvent):
    def __init__(self):
        self.todoByTab = {}
        
        import threading
        self.lock = threading.Lock()

    @dataclass
    class TabItem():
        MenuNumber : int
        Description : str
        Price : float

    @dataclass
    class TabStatus():
        TabId : uuid
        TableNumber : int
        ToServe : []
        InPreparation : []
        Served : []

    @dataclass
    class TabInvoice():
        TabId : uuid
        TableNumber : int
        Items : []
        Total : float
        HasUnservedItems : bool

    @dataclass
    class Tab():
        TableNumber : int
        Waiter : str
        ToServe : []
        InPreparation : []
        Served : []

    def ActiveTableNumbers(self):
        self.lock.acquire()
        try:
            return [self.todoByTab[tab].TableNumber for tab in self.todoByTab]
        finally:
            self.lock.release()

    def TodoListForWaiter(self, waiter):
        self.lock.acquire()
        try:
            return [{
                self.todoByTab[tab].TableNumber : [item for item in self.todoByTab[tab].ToServe]
                } for tab in self.todoByTab if self.todoByTab[tab].Waiter == waiter]
        finally:
            self.lock.release()

    def TabIdForTable(self, table):
        self.lock.acquire()
        try:
            return next(iter([tabId for tabId in self.todoByTab if self.todoByTab[tabId].TableNumber == table]), None)
        finally:
            self.lock.release()

    def TabForTable(self, table):
        self.lock.acquire()
        try:
            return next(iter([self.TabStatus(tabId,
                                self.todoByTab[tabId].TableNumber,
                                [item_to_serve for item_to_serve in self.todoByTab[tabId].ToServe],
                                [item_in_prep for item_in_prep in self.todoByTab[tabId].InPreparation],
                                [item_served for item_served in self.todoByTab[tabId].Served]
                            ) for tabId in self.todoByTab if self.todoByTab[tabId].TableNumber == table]), None)
        finally:
            self.lock.release()

    def InvoiceForTable(self, table):
        self.lock.acquire()
        try:
            return next(iter([self.TabInvoice(tabId,
                                self.todoByTab[tabId].TableNumber,
                                [item_served for item_served in self.todoByTab[tabId].Served],
                                sum([item_served.Price for item_served in self.todoByTab[tabId].Served]),
                                bool([item_to_serve for item_to_serve in self.todoByTab[tabId].ToServe] + 
                                [item_in_prep for item_in_prep in self.todoByTab[tabId].InPreparation])
                            ) for tabId in self.todoByTab if self.todoByTab[tabId].TableNumber == table]), None)
        finally:
            self.lock.release()

    @methdispatch
    def Handle(self, event):
        raise ValueError(f"Subscriber {self.__class__.__name__} does not know how to handle event {event.__class__.__name__}")

    @Handle.register(TabOpened)
    def Handle_TabOpened(self, event):
        self.lock.acquire()
        try:
            self.todoByTab[event.Id] = self.Tab(event.TableNumber, event.Waiter, [], [], [])
        finally:
            self.lock.release()

    @Handle.register(DrinksOrdered)
    def Handle_DrinksOrdered(self, event):
        self.lock.acquire()
        try:
            self.todoByTab[event.Id].ToServe += [self.TabItem(drink.MenuNumber, drink.Description, drink.Price) for drink in event.Items]
        finally:
            self.lock.release()

    @Handle.register(FoodOrdered)
    def Handle_FoodOrdered(self, event):
        self.lock.acquire()
        try:
            self.todoByTab[event.Id].InPreparation += [self.TabItem(food.MenuNumber, food.Description, food.Price) for food in event.Items]
        finally:
            self.lock.release()

    @Handle.register(FoodPrepared)
    def Handle_FoodPrepared(self, event):
        self.MoveItems(event.Id, event.MenuNumbers, lambda t : t.InPreparation, lambda t : t.ToServe)

    @Handle.register(DrinksServed)
    def Handle_DrinksServed(self, event):
        self.MoveItems(event.Id, event.MenuNumbers, lambda t : t.ToServe, lambda t : t.Served)

    @Handle.register(FoodServed)
    def Handle_FoodServed(self, event):
        self.MoveItems(event.Id, event.MenuNumbers, lambda t : t.ToServe, lambda t : t.Served)

    @Handle.register(TabClosed)
    def Handle_TabClosed(self, event):
        self.lock.acquire()
        try:
            self.todoByTab.pop(event.Id)
        finally:
            self.lock.release()

    def MoveItems(self, tabId, menuNumbers, from_expression, to_expression):
        tab = self.todoByTab[tabId]
        self.lock.acquire()
        try:
            fromList = from_expression(tab)
            toList = to_expression(tab)
            for menu_num in menuNumbers:
                tabItem = next(iter([from_item for from_item in fromList if from_item.MenuNumber == menu_num]))
                fromList.remove(tabItem)
                toList.append(tabItem)
        finally:
            self.lock.release()
