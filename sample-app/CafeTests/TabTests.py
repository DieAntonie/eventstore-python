import unittest
import uuid

class TabTests(unittest.TestCase, BDDTest):
    def setUp(self):
        self.testId = uuid.UUID()
        self.testTable = 42
        self.testWaiter = "Derek"
        self.testDrink1 = OrderedItem(4, "Sprite", 1.50, True)
        self.testDrink2 = OrderedItem(4, "Beer", 2.50, True)
        self.testFood1 = OrderedItem(4, "Beef Noodles", 7.50, False)
        self.testFood2 = OrderedItem(4, "Vegetable Curry", 6.00, False)

    def test_can_open_a_new_tab(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()