from functools import singledispatch, update_wrapper
from .Exceptions import (
    TabNotOpen,
    DrinksNotOutstanding,
    FoodNotOutstanding,
    FoodNotPrepared,
    MustPayEnough,
    TabHasUnservedItems)
from .CloseTab import CloseTab
from .MarkDrinksServed import MarkDrinksServed
from .MarkFoodPrepared import MarkFoodPrepared
from .MarkFoodServed import MarkFoodServed
from .OpenTab import OpenTab
from .PlaceOrder import PlaceOrder
from ...Edument_CQRS.Aggregate import Aggregate
from ...Edument_CQRS.IApplyEvent import IApplyEvent
from ...Edument_CQRS.IHandleCommand import IHandleCommand
from ...Events.Tab.DrinksOrdered import DrinksOrdered
from ...Events.Tab.DrinksServed import DrinksServed
from ...Events.Tab.FoodOrdered import FoodOrdered
from ...Events.Tab.FoodPrepared import FoodPrepared
from ...Events.Tab.FoodServed import FoodServed
from ...Events.Tab.TabOpened import TabOpened
from ...Events.Tab.TabClosed import TabClosed


def methdispatch(func):
    """
    Extended Single-dispatch generic class method decorator.

    Transforms a class method into a generic function, which can have different behaviours depending upon the type of its first argument. The decorated class method acts as the default implementation, and additional implementations can be registered using the `register()` attribute of the generic function.
    """
    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        """
        Generic class method wrapper.
        """
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    wrapper.register = dispatcher.register
    wrapper.registry = dispatcher.registry
    update_wrapper(wrapper, func)
    return wrapper


class TabAggregate(Aggregate, IHandleCommand, IApplyEvent):
    """
    An instance of the Tab domain object.
    """

    def __init__(self):
        super(TabAggregate, self).__init__()
        self.outstandingDrinks = []
        self.outstandingFood = []
        self.preparedFood = []
        self.open = False
        self.servedItemsValue = 0.0

    @methdispatch
    def Handle(self, command):
        """
        Generic `IHandleCommand` overloaded command handler catch all commands that are not registered to be handled.
        """
        raise ValueError(
            f"Aggregate {self.__class__.__name__} does not know how to handle command {command.__class__.__name__}")

    @Handle.register(OpenTab)
    def Handle_OpenTab(self, command: OpenTab):
        """
        `OpenTab` command handler that emits a `TabOpened` event upon successfully opening a tab.
        """
        yield TabOpened(
            command.Id,
            command.TableNumber,
            command.Waiter
        )

    @Handle.register(PlaceOrder)
    def Handle_PlaceOrder(self, command: PlaceOrder):
        """
        `PlaceOrder` command handler that emits `DrinksOrdered` and `FoodOrdered` events upon successfully placing and order.
        """
        if not self.open:
            raise TabNotOpen

        drinks = [item for item in command.Items if item.IsDrink]
        if drinks:
            yield DrinksOrdered(command.Id, drinks)

        food = [item for item in command.Items if not item.IsDrink]
        if food:
            yield FoodOrdered(command.Id, food)

    @Handle.register(MarkDrinksServed)
    def Handle_MarkDrinksServed(self, command: MarkDrinksServed):
        """
        `MarkDrinksServed` command handler that emits a `DrinksServed` event upon successfully serving drinks.
        """
        if not self.AllTheseDrinksAreOutstanding(command.MenuNumbers):
            raise DrinksNotOutstanding

        yield DrinksServed(command.Id, command.MenuNumbers)

    @Handle.register(MarkFoodPrepared)
    def Handle_MarkFoodPrepared(self, command: MarkFoodPrepared):
        """
        `MarkFoodPrepared` command handler that emits a `FoodPrepared` event upon successfully preparing food.
        """
        if not self.AllThisFoodIsOutstanding(command.MenuNumbers):
            raise FoodNotOutstanding

        yield FoodPrepared(command.Id, command.MenuNumbers)

    @Handle.register(MarkFoodServed)
    def Handle_MarkFoodServed(self, command: MarkFoodServed):
        """
        `MarkFoodServed` command handler that emits a `FoodServed` event upon successfully serving food.
        """
        if not self.AllThisFoodIsPrepared(command.MenuNumbers):
            raise FoodNotPrepared

        yield FoodServed(command.Id, command.MenuNumbers)

    @Handle.register(CloseTab)
    def Handle_CloseTab(self, command: CloseTab):
        """
        `CloseTab` command handler that emits a `TabClosed` event upon successfully closing a tab.
        """
        if not self.open:
            raise TabNotOpen
        if self.HasUnservedItems():
            raise TabHasUnservedItems
        if command.AmountPaid < self.servedItemsValue:
            raise MustPayEnough

        yield TabClosed(command.Id, command.AmountPaid, self.servedItemsValue, command.AmountPaid - self.servedItemsValue)

    def AllTheseDrinksAreOutstanding(self, menu_numbers):
        """
        Determines whether all `menu_numbers` corrospond to some outstanding drink.
        """
        return self.AreAllInList(want=menu_numbers, have=self.outstandingDrinks)

    def AllThisFoodIsOutstanding(self, menu_numbers):
        """
        Determines whether all `menu_numbers` corrospond to some outstanding food.
        """
        return self.AreAllInList(want=menu_numbers, have=self.outstandingFood)

    def AllThisFoodIsPrepared(self, menu_numbers):
        """
        Determines whether all `menu_numbers` corrospond to some prepared food.
        """
        return self.AreAllInList(want=menu_numbers, have=self.preparedFood)

    @staticmethod
    def AreAllInList(want, have):
        """
        Whether all `want` menu numbers in corrospond to atleast one indevidual `have` item.
        """
        have_menu_numbers = [have_item.MenuNumber for have_item in have]
        for want_menu_numbers in want:
            if want_menu_numbers in have_menu_numbers:
                have_menu_numbers.remove(want_menu_numbers)
            else:
                return False
        return True

    def HasUnservedItems(self):
        """
        Returns unserved items.
        """
        return self.outstandingDrinks or self.outstandingFood or self.preparedFood

    @methdispatch
    def Apply(self, event):
        """
        Generic `IApplyEvent` overloaded event handler catch all events that are not registered to be applied.
        """
        raise ValueError(
            f"Aggregate {self.__class__.__name__} does not know how to apply event {event.__class__.__name__}")

    @Apply.register(TabOpened)
    def Apply_TabOpened(self, event: TabOpened):
        """
        `TabOpened` event handler that opens this `TabAggregate`.
        """
        self.open = True

    @Apply.register(DrinksOrdered)
    def Apply_DrinksOrdered(self, event: DrinksOrdered):
        """
        `DrinksOrdered` event handler that orders this `TabAggregate`'s drink items.
        """
        self.outstandingDrinks += event.Items

    @Apply.register(FoodOrdered)
    def Apply_FoodOrdered(self, event: FoodOrdered):
        """
        `FoodOrdered` event handler that orders this `TabAggregate`'s food items.
        """
        self.outstandingFood += event.Items

    @Apply.register(DrinksServed)
    def Apply_DrinksServed(self, event: DrinksServed):
        """
        `DrinksServed` event handler that serves this `TabAggregate`'s outstanding drinks.
        """
        for num in event.MenuNumbers:
            item = next(
                drink
                for drink in self.outstandingDrinks
                if drink.MenuNumber == num
            )
            self.outstandingDrinks.remove(item)
            self.servedItemsValue += item.Price

    @Apply.register(FoodPrepared)
    def Apply_FoodPrepared(self, event: FoodPrepared):
        """
        `FoodPrepared` event handler that prepares this `TabAggregate`'s outstanding food.
        """
        for num in event.MenuNumbers:
            item = next(
                food
                for food in self.outstandingFood
                if food.MenuNumber == num)
            self.outstandingFood.remove(item)
            self.preparedFood.append(item)

    @Apply.register(FoodServed)
    def Apply_FoodServed(self, event: FoodServed):
        """
        `FoodServed` event handler that serves this `TabAggregate`'s prepared food.
        """
        for num in event.MenuNumbers:
            item = next(
                food
                for food in self.preparedFood
                if food.MenuNumber == num)
            self.preparedFood.remove(item)
            self.servedItemsValue += item.Price

    @Apply.register(TabClosed)
    def Apply_TabClosed(self, event: TabClosed):
        """
        `TabClosed` event handler that closes this `TabAggregate`.
        """
        self.open = False
