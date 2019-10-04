import unittest
import uuid
from ..Cafe.Tab.CloseTab import CloseTab
from ..Cafe.Tab.Exceptions import (
    TabNotOpen,
    DrinksNotOutstanding,
    FoodNotOutstanding,
    FoodNotPrepared,
    MustPayEnough,
    TabHasUnservedItems)
from ..Cafe.Tab.MarkDrinksServed import MarkDrinksServed
from ..Cafe.Tab.MarkFoodPrepared import MarkFoodPrepared
from ..Cafe.Tab.MarkFoodServed import MarkFoodServed
from ..Cafe.Tab.OpenTab import OpenTab
from ..Cafe.Tab.PlaceOrder import PlaceOrder
from ..Events.Tab.DrinksOrdered import DrinksOrdered
from ..Events.Tab.DrinksServed import DrinksServed
from ..Events.Tab.FoodOrdered import FoodOrdered
from ..Events.Tab.FoodPrepared import FoodPrepared
from ..Events.Tab.FoodServed import FoodServed
from ..Events.Tab.TabClosed import TabClosed
from ..Events.Tab.TabOpened import TabOpened
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

    def test_can_open_tab(self):
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

    def test_cannot_order_unopened_tab(self):
        self.BDDTest.Test(
            self.BDDTest.Given(),
            self.BDDTest.When(
                PlaceOrder(
                    self.testId,
                    [self.testDrink1]
                )
                ),
            self.BDDTest.ThenFailWith(TabNotOpen)
            )

    def test_can_order_drinks(self):
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

    def test_can_order_food(self):
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

    def test_can_order_food_and_drinks(self):
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

    def test_can_serve_ordered_drinks(self):
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

    def test_cannot_serve_unordered_drink(self):
        self.BDDTest.Test(
            self.BDDTest.Given(
                TabOpened(
                    self.testId,
                    self.testTable,
                    self.testWaiter),
                DrinksOrdered(
                    self.testId,
                    [self.testDrink1]
                )
            ),
            self.BDDTest.When(
                MarkDrinksServed(
                    self.testId,
                    [self.testDrink2.MenuNumber]
                )
            ),
            self.BDDTest.ThenFailWith(DrinksNotOutstanding)
            )

    def test_cannot_serve_drinks_twice(self):
        self.BDDTest.Test(
            self.BDDTest.Given(
                TabOpened(
                    self.testId,
                    self.testTable,
                    self.testWaiter
                ),
                DrinksOrdered(
                    self.testId,
                    [self.testDrink1]
                ),
                DrinksServed(
                    self.testId,
                    [self.testDrink1.MenuNumber]
                )
            ),
            self.BDDTest.When(
                MarkDrinksServed(
                    self.testId,
                    [self.testDrink1.MenuNumber]
                )
            ),
            self.BDDTest.ThenFailWith(DrinksNotOutstanding)
            )

    def test_can_prepare_ordered_food(self):
        self.BDDTest.Test(
            self.BDDTest.Given(
                TabOpened(
                    self.testId,
                    self.testTable,
                    self.testWaiter
                ),
                FoodOrdered(
                    self.testId,
                    [self.testFood1, self.testFood2]
                )
            ),
            self.BDDTest.When(
                MarkFoodPrepared(
                    self.testId,
                    [self.testFood1.MenuNumber, self.testFood2.MenuNumber]
                )
            ),
            self.BDDTest.Then(
                FoodPrepared(
                    self.testId,
                    [self.testFood1.MenuNumber, self.testFood2.MenuNumber]
                )
            )
        )

    def test_cannot_prepare_unordered_food(self):
        self.BDDTest.Test(
            self.BDDTest.Given(
                TabOpened(
                    self.testId,
                    self.testTable,
                    self.testWaiter
                ),
                FoodOrdered(
                    self.testId,
                    [self.testFood1]
                )
            ),
            self.BDDTest.When(
                MarkFoodPrepared(
                    self.testId,
                    [self.testFood2.MenuNumber]
                )
            ),
            self.BDDTest.ThenFailWith(FoodNotOutstanding)
        )

    def test_cannot_prepare_food_twice(self):
        self.BDDTest.Test(
            self.BDDTest.Given(
                TabOpened(
                    self.testId,
                    self.testTable,
                    self.testWaiter
                ),
                FoodOrdered(
                    self.testId,
                    [self.testFood1]
                ),
                FoodPrepared(
                    self.testId,
                    [self.testFood1.MenuNumber]
                )
            ),
            self.BDDTest.When(
                MarkFoodPrepared(
                    self.testId,
                    [self.testFood1.MenuNumber]
                )
            ),
            self.BDDTest.ThenFailWith(FoodNotOutstanding)
        )

    def test_can_serve_prepared_food(self):
        self.BDDTest.Test(
            self.BDDTest.Given(
                TabOpened(
                    self.testId,
                    self.testTable,
                    self.testWaiter
                ),
                FoodOrdered(
                    self.testId,
                    [self.testFood1, self.testFood2]
                ),
                FoodPrepared(
                    self.testId,
                    [self.testFood1.MenuNumber, self.testFood2.MenuNumber]
                )
            ),
            self.BDDTest.When(
                MarkFoodServed(
                    self.testId,
                    [self.testFood1.MenuNumber, self.testFood2.MenuNumber]
                )
            ),
            self.BDDTest.Then(
                FoodServed(
                    self.testId,
                    [self.testFood1.MenuNumber, self.testFood2.MenuNumber]
                )
            )
        )

    def test_cannot_serve_food_twice(self):
        self.BDDTest.Test(
            self.BDDTest.Given(
                TabOpened(
                    self.testId,
                    self.testTable,
                    self.testWaiter
                ),
                FoodOrdered(
                    self.testId,
                    [self.testFood1]
                ),
                FoodPrepared(
                    self.testId,
                    [self.testFood1.MenuNumber]
                ),
                FoodServed(
                    self.testId,
                    [self.testFood1.MenuNumber]
                )
            ),
            self.BDDTest.When(
                MarkFoodServed(
                    self.testId,
                    [self.testFood1.MenuNumber]
                )
            ),
            self.BDDTest.ThenFailWith(FoodNotPrepared)
        )

    def test_cannot_serve_unprepared_food(self):
        self.BDDTest.Test(
            self.BDDTest.Given(
                TabOpened(
                    self.testId,
                    self.testTable,
                    self.testWaiter
                ),
                FoodOrdered(
                    self.testId,
                    [self.testFood1]
                )
            ),
            self.BDDTest.When(
                MarkFoodServed(
                    self.testId,
                    [self.testFood1.MenuNumber]
                )
            ),
            self.BDDTest.ThenFailWith(FoodNotPrepared)
        )

    def test_cannot_serve_unordered_food(self):
        self.BDDTest.Test(
            self.BDDTest.Given(
                TabOpened(
                    self.testId,
                    self.testTable,
                    self.testWaiter
                ),
                FoodOrdered(
                    self.testId,
                    [self.testFood1]
                )
            ),
            self.BDDTest.When(
                MarkFoodServed(
                    self.testId,
                    [self.testFood2.MenuNumber]
                )
            ),
            self.BDDTest.ThenFailWith(FoodNotPrepared)
        )

    def test_can_close_tab_exact_amount(self):
        self.BDDTest.Test(
            self.BDDTest.Given(
                TabOpened(
                    self.testId,
                    self.testTable,
                    self.testWaiter
                ),
                FoodOrdered(
                    self.testId,
                    [self.testFood1, self.testFood2]
                ),
                FoodPrepared(
                    self.testId,
                    [self.testFood1.MenuNumber, self.testFood2.MenuNumber]
                ),
                FoodServed(
                    self.testId,
                    [self.testFood1.MenuNumber, self.testFood2.MenuNumber]
                )
            ),
            self.BDDTest.When(
                CloseTab(
                    self.testId,
                    self.testFood1.Price + self.testFood2.Price
                )
            ),
            self.BDDTest.Then(
                TabClosed(
                    self.testId,
                    self.testFood1.Price + self.testFood2.Price,
                    self.testFood1.Price + self.testFood2.Price,
                    0.0
                )
            )
        )

    def test_can_close_tab_with_tip(self):
        self.BDDTest.Test(
            self.BDDTest.Given(
                TabOpened(
                    self.testId,
                    self.testTable,
                    self.testWaiter
                ),
                FoodOrdered(
                    self.testId,
                    [self.testFood1, self.testFood2]
                ),
                FoodPrepared(
                    self.testId,
                    [self.testFood1.MenuNumber, self.testFood2.MenuNumber]
                ),
                FoodServed(
                    self.testId,
                    [self.testFood1.MenuNumber, self.testFood2.MenuNumber]
                )
            ),
            self.BDDTest.When(
                CloseTab(
                    self.testId,
                    self.testFood1.Price + self.testFood2.Price + 0.50
                )
            ),
            self.BDDTest.Then(
                TabClosed(
                    self.testId,
                    self.testFood1.Price + self.testFood2.Price + 0.50,
                    self.testFood1.Price + self.testFood2.Price,
                    0.50
                )
            )
        )

    def test_cannot_close_tab_with_less(self):
        self.BDDTest.Test(
            self.BDDTest.Given(
                TabOpened(
                    self.testId,
                    self.testTable,
                    self.testWaiter
                ),
                FoodOrdered(
                    self.testId,
                    [self.testFood1, self.testFood2]
                ),
                FoodPrepared(
                    self.testId,
                    [self.testFood1.MenuNumber, self.testFood2.MenuNumber]
                ),
                FoodServed(
                    self.testId,
                    [self.testFood1.MenuNumber, self.testFood2.MenuNumber]
                )
            ),
            self.BDDTest.When(
                CloseTab(
                    self.testId,
                    self.testFood1.Price + self.testFood2.Price - 0.50
                )
            ),
            self.BDDTest.ThenFailWith(MustPayEnough)
        )

    def test_cannot_close_tab_twice(self):
        self.BDDTest.Test(
            self.BDDTest.Given(
                TabOpened(
                    self.testId,
                    self.testTable,
                    self.testWaiter
                ),
                FoodOrdered(
                    self.testId,
                    [self.testFood1, self.testFood2]
                ),
                FoodPrepared(
                    self.testId,
                    [self.testFood1.MenuNumber, self.testFood2.MenuNumber]
                ),
                FoodServed(
                    self.testId,
                    [self.testFood1.MenuNumber, self.testFood2.MenuNumber]
                ),
                TabClosed(
                    self.testId,
                    self.testFood1.Price + self.testFood2.Price + 0.50,
                    self.testFood1.Price + self.testFood2.Price,
                    0.50
                )
            ),
            self.BDDTest.When(
                CloseTab(
                    self.testId,
                    self.testFood1.Price + self.testFood2.Price
                )
            ),
            self.BDDTest.ThenFailWith(TabNotOpen)
        )

if __name__ == '__main__':
    unittest.main()