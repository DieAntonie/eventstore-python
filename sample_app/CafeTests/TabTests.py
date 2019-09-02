import unittest
import uuid
from ..Cafe.Tab.OpenTab import OpenTab
from ..Events.Tab.TabOpened import TabOpened
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

if __name__ == '__main__':
    unittest.main()