# from dataclasses import dataclass
from src.Infrastructure.MessageDispatcher import MessageDispatcher
from src.Infrastructure.SqlEventStore import SqlEventStore
# from src.Cafe.ReadModels.OpenTabs import OpenTabs
# from src.Cafe.ReadModels.ChefTodoList import ChefTodoList
# from src.Cafe.Tab.Commands.CloseTab import CloseTab
# from src.Cafe.Tab.Commands.MarkDrinksServed import MarkDrinksServed
# from src.Cafe.Tab.Commands.MarkFoodPrepared import MarkFoodPrepared
# from src.Cafe.Tab.Commands.MarkFoodServed import MarkFoodServed
from src.DungeonsDragons.Character.Commands.SetCharacterRace import SetCharacterRace
from src.DungeonsDragons.Game.Race.Race import Dragonborn
from src.DungeonsDragons.Game.Alignment import Alignment
# from src.Cafe.Tab.Commands.PlaceOrder import PlaceOrder
# from src.Cafe.Tab.Shared import OrderedItem
from src.DungeonsDragons.Character.CharacterAggregate import CharacterAggregate
import uuid


# # Create Message dispatcher and set source to PSQL Event store.
Dispatcher = MessageDispatcher(SqlEventStore())

# # Scan the a Tab Aggregate to register all command handlers.
Dispatcher.RegisterHandlersOfInstance(CharacterAggregate())

# # Scan the OpenTabs read model to register all subscription handlers.
# OpenTabQueries = OpenTabs()
# Dispatcher.RegisterHandlersOfInstance(OpenTabQueries)

# # Scan the ChefTodoList read model to register all subscription handlers.
# ChefTodoListQueries = ChefTodoList()
# Dispatcher.RegisterHandlersOfInstance(ChefTodoListQueries)

# #
Tab_Key = uuid.uuid1()

# # Print State
# print("### Part 0: Current state")
# print(f"-->  Active Tables Numbers are: {OpenTabQueries.ActiveTableNumbers()}")
# todo_list = OpenTabQueries.TodoListForWaiter("Chris")
# print(f"-->  Todo List For Waiter is: {todo_list}")
# print(f"-->  Todo List For Chef is: {ChefTodoListQueries.GetTodoList()}")z

# # We start by opening a tab for table 3, served by Chris.
print("### Part 1: Open a new Tab on table 3 for waiter Chris")
set_race = SetCharacterRace(
    Id=Tab_Key,
    Race=Dragonborn.Green,
    Age=50,
    Alignment=Alignment.Neutral
)

Dispatcher.SendCommand(set_race)

# # Print State
# print(f"-->  Active Tables Numbers are: {OpenTabQueries.ActiveTableNumbers()}")
# todo_list = OpenTabQueries.TodoListForWaiter("Chris")
# print(f"-->  Todo List For Waiter is: {todo_list}")
# print(f"-->  Todo List For Chef is: {ChefTodoListQueries.GetTodoList()}")
# print(f"-->  Tab ID for table is: {OpenTabQueries.TabIdForTable(3)}")
# print(f"-->  Tab for table is: {OpenTabQueries.TabForTable(3)}")
# print(f"-->  Invoice for table is: {OpenTabQueries.InvoiceForTable(3)}")

# # Decide on the order items
# print("### Part 2: Order 4 Items [Steak, Ribs, Beer, Beer]")
# my_steak_order = OrderedItem(
#     MenuNumber=2,
#     Description="Steak",
#     IsDrink=False,
#     Price=100.00
# )

# your_ribs_order = OrderedItem(
#     MenuNumber=1,
#     Description="Ribs",
#     IsDrink=False,
#     Price=120.00
# )

# my_beer_order = OrderedItem(
#     MenuNumber=40,
#     Description="Beer",
#     IsDrink=True,
#     Price=25.00
# )

# your_beer_order = OrderedItem(
#     MenuNumber=40,
#     Description="Beer",
#     IsDrink=True,
#     Price=25.00
# )

# # Place order for decided on order items
# place_an_order = PlaceOrder(Id=Tab_Key,
#                             Items=[
#                                 my_steak_order,
#                                 your_ribs_order,
#                                 my_beer_order,
#                                 your_beer_order
#                             ])
# Dispatcher.SendCommand(place_an_order)

# # Print State
# todo_list = OpenTabQueries.TodoListForWaiter("Chris")
# print(f"-->  Todo List For Waiter is: {todo_list}")
# print(f"-->  Todo List For Chef is: {ChefTodoListQueries.GetTodoList()}")
# print(f"-->  Tab ID for table is: {OpenTabQueries.TabIdForTable(3)}")
# print(f"-->  Tab for table is: {OpenTabQueries.TabForTable(3)}")
# print(f"-->  Invoice for table is: {OpenTabQueries.InvoiceForTable(3)}")

# print("### Part 3: Serve the beers")
# drinks_menu_numbers = [
#     waiter_item[3]
#     for waiter_item in todo_list
#     if waiter_item.get(3)
# ][0]
# serve_drinks = MarkDrinksServed(Id=Tab_Key,
#                                 MenuNumbers=[
#                                     drinks.MenuNumber
#                                     for drinks in drinks_menu_numbers
#                                 ])
# Dispatcher.SendCommand(serve_drinks)

# # Print State
# todo_list = OpenTabQueries.TodoListForWaiter("Chris")
# print(f"-->  Todo List For Waiter is: {todo_list}")
# print(f"-->  Todo List For Chef is: {ChefTodoListQueries.GetTodoList()}")
# print(f"-->  Tab ID for table is: {OpenTabQueries.TabIdForTable(3)}")
# print(f"-->  Tab for table is: {OpenTabQueries.TabForTable(3)}")
# print(f"-->  Invoice for table is: {OpenTabQueries.InvoiceForTable(3)}")

# print("### Part 4: Prepare the food")
# chef_todo_list_group = ChefTodoListQueries.GetTodoList()[0]
# prepare_food = MarkFoodPrepared(Id=Tab_Key,
#                                 MenuNumbers=[
#                                     chef_item.MenuNumber
#                                     for chef_item in chef_todo_list_group.Items
#                                 ])
# Dispatcher.SendCommand(prepare_food)

# # Print State
# todo_list = OpenTabQueries.TodoListForWaiter("Chris")
# print(f"-->  Todo List For Waiter is: {todo_list}")
# print(f"-->  Todo List For Chef is: {ChefTodoListQueries.GetTodoList()}")
# print(f"-->  Tab ID for table is: {OpenTabQueries.TabIdForTable(3)}")
# print(f"-->  Tab for table is: {OpenTabQueries.TabForTable(3)}")
# print(f"-->  Invoice for table is: {OpenTabQueries.InvoiceForTable(3)}")

# print("### Part 5: Serve the food")
# food_menu_numbers = [
#     waiter_item[3]
#     for waiter_item in todo_list
#     if waiter_item.get(3)
# ][0]
# serve_food = MarkFoodServed(Id=Tab_Key,
#                             MenuNumbers=[
#                                 food.MenuNumber
#                                 for food in food_menu_numbers
#                             ])
# Dispatcher.SendCommand(serve_food)

# # Print State
# todo_list = OpenTabQueries.TodoListForWaiter("Chris")
# print(f"-->  Todo List For Waiter is: {todo_list}")
# print(f"-->  Todo List For Chef is: {ChefTodoListQueries.GetTodoList()}")
# print(f"-->  Tab ID for table is: {OpenTabQueries.TabIdForTable(3)}")
# print(f"-->  Tab for table is: {OpenTabQueries.TabForTable(3)}")
# print(f"-->  Invoice for table is: {OpenTabQueries.InvoiceForTable(3)}")

# print("### Part 6: Close the tab")
# amount_to_pay = sum([
#     invoice_item.Price
#     for invoice_item in OpenTabQueries.InvoiceForTable(3).Items
# ]) + 50
# close_tab = CloseTab(Id=Tab_Key, AmountPaid=amount_to_pay)
# Dispatcher.SendCommand(close_tab)

# # Print State
# todo_list = OpenTabQueries.TodoListForWaiter("Chris")
# print(f"-->  Todo List For Waiter is: {todo_list}")
# print(f"-->  Todo List For Chef is: {ChefTodoListQueries.GetTodoList()}")
# print(f"-->  Tab ID for table is: {OpenTabQueries.TabIdForTable(3)}")
# print(f"-->  Tab for table is: {OpenTabQueries.TabForTable(3)}")
# print(f"-->  Invoice for table is: {OpenTabQueries.InvoiceForTable(3)}")
