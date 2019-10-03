import unittest
import uuid
from ..Cafe.Tab.OpenTab import OpenTab
from ..Cafe.Tab.PlaceOrder import PlaceOrder
from ..Events.Tab.TabOpened import TabOpened
from ..Events.Tab.DrinksOrdered import DrinksOrdered
from ..Edument_CQRS.BDDTest import BDDTest
from ..Events.Tab.Shared import OrderedItem

class TabTests(unittest.TestCase):
    def setUp(self):
        self.BDDTest = BDDTest(self)
        self.testId = uuid.uuid1()
        self.testTable = 42
        self.testWaiter = "Derek"
        self.testDrink1 = OrderedItem(4, "Sprite", 1.50, True)
        self.testDrink2 = OrderedItem(4, "Beer", 2.50, True)
        self.testFood1 = OrderedItem(4, "Beef Noodles", 7.50, False)
        self.testFood2 = OrderedItem(4, "Vegetable Curry", 6.00, False)

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

if __name__ == '__main__':
    unittest.main()