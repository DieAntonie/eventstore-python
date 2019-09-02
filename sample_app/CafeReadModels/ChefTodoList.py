from dataclasses import dataclass
from functools import singledispatch
from IChefTodoListQueries import IChefTodoListQueries
import uuid

class ChefTodoList(IChefTodoListQueries, ISubscribeTo):
    def __init__(self):
        self.todoList = []
        
        import threading
        self.lock = threading.Lock()

    @dataclass
    class TodoListItem():
        MenuNumber : int
        Description : str

    @dataclass
    class TodoListGroup():
        Tab : uuid
        Items : []


    def GetTodoList(self):
        self.lock.acquire()
        try:
            return [self.TodoListGroup(item.Tab, item.Items) for item in self.todoList]
        finally:
            self.lock.release()

    @singledispatch
    def Handle(self, event):
        raise ValueError(f"Subscriber {self.__class__.__name__} does not know how to handle event {event.__class__.__name__}")

    @Handle.register(FoodOrdered)
    def Handle_FoodOrdered(self, event):
        group = self.TodoListGroup(event.Id, [self.TodoListItem(item.MenuNumber, item.Description) for item in event.items])
        self.lock.acquire()
        try:
            self.todoList.append(group)
        finally:
            self.lock.release()


    @Handle.register(FoodPrepared)
    def Handle_FoodPrepared(self, event):
        self.lock.acquire()
        try:
            group = next([todo_group for todo_group in self.todoList if todo_group.Tab == event.Id])

            for menu_number in event.MenuNumbers:
                group.Items.remove(next([remove_item for remove_item in group.Items if remove_item.MenuNumber == menu_number]))
            
            if group.Items == []:
                self.todoList.remove(group)
        finally:
            self.lock.release()
