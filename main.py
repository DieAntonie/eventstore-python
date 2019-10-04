from dataclasses import dataclass
from sample_app.Edument_CQRS.MessageDispatcher import MessageDispatcher
from sample_app.Edument_CQRS.SqlEventStore import SqlEventStore
from sample_app.CafeReadModels.OpenTabs import OpenTabs
from sample_app.CafeReadModels.ChefTodoList import ChefTodoList
from sample_app.Cafe.Tab.TabAggregate import TabAggregate
from sample_app.Cafe.Tab.MarkDrinksServed import MarkDrinksServed
from sample_app.Cafe.Tab.MarkFoodPrepared import MarkFoodPrepared
from sample_app.Cafe.Tab.MarkFoodServed import MarkFoodServed
from sample_app.Cafe.Tab.OpenTab import OpenTab
from sample_app.Cafe.Tab.PlaceOrder import PlaceOrder
from sample_app.Events.Tab.Shared import OrderedItem
import uuid


# Create Message dispatcher and set source to PSQL Event store.
Dispatcher = MessageDispatcher(SqlEventStore())

# Scan the a Tab Aggregate to register all command handlers.
Dispatcher.ScanInstance(TabAggregate())

# Scan the OpenTabs read model to register all subscription handlers.
OpenTabQueries = OpenTabs()
Dispatcher.ScanInstance(OpenTabQueries)

# Scan the ChefTodoList read model to register all subscription handlers.
ChefTodoListQueries = ChefTodoList()
Dispatcher.ScanInstance(ChefTodoListQueries)

# 
Tab_Key = uuid.uuid1()

# We start by opening a tab for table 3, served by Chris.
open_a_tab = OpenTab(Id=Tab_Key, TableNumber=3, Waiter="Chris")

# We send the command to the dispatcher, to apply to the appropriate handlers.
Dispatcher.SendCommand(open_a_tab)

# Decide on the order items
my_steak = OrderedItem(
    MenuNumber=2,
    Description="Steak",
    IsDrink=False,
    Price=100.00
    )

your_ribs = OrderedItem(
    MenuNumber=1,
    Description="Ribs",
    IsDrink=False,
    Price=120.00
    )

my_beer = OrderedItem(
    MenuNumber=40,
    Description="Beer",
    IsDrink=False,
    Price=25.00
    )

your_beer = OrderedItem(
    MenuNumber=40,
    Description="Beer",
    IsDrink=False,
    Price=25.00
    )

# Place order for decided on order items
place_an_order = PlaceOrder(Id=Tab_Key, Items=[my_steak, your_ribs, my_beer, your_beer])
Dispatcher.SendCommand(place_an_order)


