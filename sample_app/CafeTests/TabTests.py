import unittest
import uuid
from ..Cafe.Tab.OpenTab import OpenTab
from ..Cafe.Tab.PlaceOrder import PlaceOrder
from ..Events.Tab.TabOpened import TabOpened
from ..Events.Tab.DrinksOrdered import DrinksOrdered
from ..Events.Tab.FoodOrdered import FoodOrdered
from ..Edument_CQRS.BDDTest import BDDTest
from ..Events.Tab.Shared import OrderedItem

class TabTests(unittest.TestCase):
    def setUp(self):
        self.BDDTest = BDDTest(self)
        self.testId = uuid.uuid1()
        self.testTable = 42
        self.testWaiter = "Derek"
        self.testDrink1 = OrderedItem(4, "Sprite", True, 1.50)
        self.testDrink2 = OrderedItem(4, "Beer", True, 2.50)
        self.testFood1 = OrderedItem(4, "Beef Noodles", False, 7.50)
        self.testFood2 = OrderedItem(4, "Vegetable Curry", False, 6.00)

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

if __name__ == '__main__':
    unittest.main()