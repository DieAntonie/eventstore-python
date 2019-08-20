from functools import singledispatch
from Exceptions import *
from CloseTab import CloseTab
from MarkDrinksServed import MarkDrinksServed
from MarkFoodPrepared import MarkFoodPrepared
from MarkFoodServed import MarkFoodServed
from OpenTab import OpenTab
from PlaceOrder import PlaceOrder

class TabAggregate(Aggregate, IHandleCommand, IApplyEvent):
    def __init__(self, ):
        self.outstandingDrinks = []
        self.outstandingFood = []
        self.preparedFood = []
        self.open = False
        self.servedItemsValue = 0.0

    @singledispatch
    def Handle(self, command):
        raise ValueError(f"Aggregate {self.__class__.__name__} does not know how to handle command {command.__class__.__name__}")

    @Handle.register(OpenTab)
    def Handle_OpenTab(self, command):
        yield TabOpened(
            command.Id,
            command.TableNumber,
            command.Waiter
        )

    @Handle.register(PlaceOrder)
    def Handle_PlaceOrder(self, command):
        if not self.open:
            raise TabNotOpen

        drinks = [item for item in command.Items if item.IsDrink]
        if drinks:
            yield DrinksOrdered(command.Id, drinks)

        food = [item for item in command.Items if not item.IsDrink]
        if food:
            yield FoodOrdered(command.Id, food)

    @Handle.register(MarkDrinksServed)
    def Handle_MarkDrinksServed(self, command):
        if not self.AreDrinksOutstanding(command.MenuNumbers):
            raise DrinksNotOutstanding

        yield DrinksServed(command.Id, command.MenuNumbers)

    @Handle.register(MarkFoodPrepared)
    def Handle_MarkFoodPrepared(self, command):
        if not self.IsFoodOutstanding(command.MenuNumbers):
            raise FoodNotOutstanding

        yield FoodPrepared(command.Id, command.MenuNumbers)

    @Handle.register(MarkFoodServed)
    def Handle_MarkFoodServed(self, command):
        if not self.IsFoodPrepared(command.MenuNumbers):
            raise FoodNotPrepared

        yield FoodServed(command.Id, command.MenuNumbers)

    @Handle.register(CloseTab)
    def Handle_CloseTab(self, command):
        if not self.open:
            raise TabNotOpen
        if self.HasUnservedItems():
            raise TabHasUnservedItems
        if command.AmountPaid < self.servedItemsValue:
            raise MustPayEnough

        yield TabClosed(command.Id, command.AmountPaid, self.servedItemsValue, command.AmountPaid - self.servedItemsValue)

    def AreDrinksOutstanding(self, menuNumbers):
        return self.AreAllInList(want = menuNumbers, have = self.outstandingDrinks)

    def IsFoodOutstanding(self, menuNumbers):
        return self.AreAllInList(want = menuNumbers, have = self.outstandingFood)

    def IsFoodPrepared(self, menuNumbers):
        return self.AreAllInList(want = menuNumbers, have = self.preparedFood)

    @staticmethod
    def AreAllInList(want, have):
        curHave = [item.MenuNumber for item in have]
        for num in want:
            if num in curHave:
                curHave.remove(num)
            else:
                return False
        return True

    def HasUnservedItems(self):
        return self.outstandingDrinks or self.outstandingFood or self.preparedFood

    @singledispatch
    def Apply(self, event):
        raise ValueError(f"Aggregate {self.__class__.__name__} does not know how to apply event {event.__class__.__name__}")

    @Apply.register(TabOpened)
    def Apply_TabOpened(self, event):
        self.open = True

    @Apply.register(DrinksOrdered)
    def Apply_DrinksOrdered(self, event):
        self.outstandingDrinks += event.Items

    @Apply.register(FoodOrdered)
    def Apply_FoodOrdered(self, event):
        self.outstandingFood += event.Items

    @Apply.register(DrinksServed)
    def Apply_DrinksServed(self, event):
        for num in event.MenuNumbers:
            item = next(drink for drink in self.outstandingDrinks if drink.MenuNumber == num)
            self.outstandingDrinks.remove(item)
            self.servedItemsValue += item.Price

    @Apply.register(FoodPrepared)
    def Apply_FoodPrepared(self, event):
        for num in event.MenuNumbers:
            item = next(food for food in self.outstandingFood if food.MenuNumber == num)
            self.outstandingFood.remove(item)
            self.preparedFood.append(item)

    @Apply.register(FoodServed)
    def Apply_FoodServed(self, event):
        for num in event.MenuNumbers:
            item = next(food for food in self.preparedFood if food.MenuNumber == num)
            self.preparedFood.remove(item)
            self.servedItemsValue += item.Price

    @Apply.register(TabClosed)
    def Apply_TabClosed(self, event):
        self.open = False
