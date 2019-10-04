from sample_app.Edument_CQRS.MessageDispatcher import MessageDispatcher
from sample_app.Edument_CQRS.SqlEventStore import SqlEventStore
from sample_app.CafeReadModels.OpenTabs import OpenTabs
from sample_app.CafeReadModels.ChefTodoList import ChefTodoList
from sample_app.Cafe.Tab.TabAggregate import TabAggregate

Dispatcher = MessageDispatcher(SqlEventStore())

Dispatcher.ScanInstance(TabAggregate())

OpenTabQueries = OpenTabs()
Dispatcher.ScanInstance(OpenTabQueries)

ChefTodoListQueries = ChefTodoList()
Dispatcher.ScanInstance(ChefTodoListQueries)





