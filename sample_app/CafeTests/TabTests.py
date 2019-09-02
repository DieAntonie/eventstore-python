import unittest
import uuid
from ..Events.Tab.Shared import OrderedItem

class TabTests(unittest.TestCase):
    def setUp(self):
        self.testId = uuid.uuid1()
        self.testTable = 42
        self.testWaiter = "Derek"
        self.testDrink1 = OrderedItem(4, "Sprite", 1.50, True)
        self.testDrink2 = OrderedItem(4, "Beer", 2.50, True)
        self.testFood1 = OrderedItem(4, "Beef Noodles", 7.50, False)
        self.testFood2 = OrderedItem(4, "Vegetable Curry", 6.00, False)

if __name__ == '__main__':
    unittest.main()