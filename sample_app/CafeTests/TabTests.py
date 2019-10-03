import unittest
import uuid
from ..Cafe.Tab.Exceptions import (
    TabNotOpen,
    DrinksNotOutstanding,
    FoodNotOutstanding,
    FoodNotPrepared,
    MustPayEnough,
    TabHasUnservedItems)
from ..Cafe.Tab.OpenTab import OpenTab
from ..Cafe.Tab.PlaceOrder import PlaceOrder
from ..Cafe.Tab.MarkDrinksServed import MarkDrinksServed
from ..Events.Tab.TabOpened import TabOpened
from ..Events.Tab.DrinksOrdered import DrinksOrdered
from ..Events.Tab.FoodOrdered import FoodOrdered
from ..Events.Tab.DrinksServed import DrinksServed
from ..Edument_CQRS.BDDTest import BDDTest
from ..Events.Tab.Shared import OrderedItem

class TabTests(unittest.TestCase):
    def setUp(self):
        self.BDDTest = BDDTest(self)
        self.testId = uuid.uuid1()
        self.testTable = 42
        self.testWaiter = "Derek"
        self.testDrink1 = OrderedItem(4, "Sprite", True, 1.50)
        self.testDrink2 = OrderedItem(10, "Beer", True, 2.50)
        self.testFood1 = OrderedItem(16, "Beef Noodles", False, 7.50)
        self.testFood2 = OrderedItem(25, "Vegetable Curry", False, 6.00)

    def test_can_open_a_new_tab(self):
        self.BDDTest.Test(
            self.BDDTest.Given(),
            self.BDDTest.When(
                OpenTab(
                    self.testId,
                    self.testTable,
                    self.testWaiter
                    )
                ),
            self.BDDTest.Then(
                TabOpened(
                    self.testId,
                    self.testTable,
                    self.testWaiter
                    )
                )
            )

    def test_can_place_drinks_order(self):
        self.BDDTest.Test(
            self.BDDTest.Given(TabOpened(
                self.testId,
                self.testTable,
                self.testWaiter
            )),
            self.BDDTest.When(
                PlaceOrder(
                    self.testId,
                    [self.testDrink1, self.testDrink2]
                )
                ),
            self.BDDTest.Then(
                DrinksOrdered(
                    self.testId,
                    [self.testDrink1, self.testDrink2]
                    )
                )
            )

    def test_can_place_food_order(self):
        self.BDDTest.Test(
            self.BDDTest.Given(TabOpened(
                self.testId,
                self.testTable,
                self.testWaiter
            )),
            self.BDDTest.When(
                PlaceOrder(
                    self.testId,
                    [self.testFood1, self.testFood2]
                )
                ),
            self.BDDTest.Then(
                FoodOrdered(
                    self.testId,
                    [self.testFood1, self.testFood2]
                    )
                )
            )

    def test_can_place_food_and_drink_order(self):
        self.BDDTest.Test(
            self.BDDTest.Given(TabOpened(
                self.testId,
                self.testTable,
                self.testWaiter
            )),
            self.BDDTest.When(
                PlaceOrder(
                    self.testId,
                    [self.testDrink2, self.testFood1]
                )
                ),
            self.BDDTest.Then(
                FoodOrdered(
                    self.testId,
                    [self.testFood1]
                    ),
                DrinksOrdered(
                    self.testId,
                    [self.testDrink2]
                    )
                )
            )

    def test_ordered_drinks_can_be_served(self):
        self.BDDTest.Test(
            self.BDDTest.Given(
                TabOpened(
                    self.testId,
                    self.testTable,
                    self.testWaiter),
                DrinksOrdered(
                    self.testId,
                    [self.testDrink1, self.testDrink2]
                    )
                ),
            self.BDDTest.When(
                MarkDrinksServed(
                    self.testId,
                    [self.testDrink1.MenuNumber, self.testDrink2.MenuNumber]
                )
            ),
            self.BDDTest.Then(
                DrinksServed(
                    self.testId,
                    [self.testDrink1.MenuNumber, self.testDrink2.MenuNumber]
                    )
                )
            )

if __name__ == '__main__':
    unittest.main()