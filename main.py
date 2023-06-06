from src.DungeonsDragons.ReadModels.RaceReadModel import RaceReadModel
from src.Infrastructure.MessageDispatcher import MessageDispatcher
from src.Infrastructure.SqlEventStore import SqlEventStore
from src.DungeonsDragons.Game.Race.RaceAggregate import RaceAggregate

print("### Part 1: Setup Dispatcher and register handlers")
# Create Message dispatcher and set source to PSQL Event store.
Dispatcher = MessageDispatcher(SqlEventStore())

# Scan the Race Aggregate to register all command and event handlers.
race_aggregate = RaceAggregate()
Dispatcher.RegisterHandlersOfInstance(race_aggregate)

# Scan the Races ReadModel to register all event handlers.
race_read_model = RaceReadModel()
Dispatcher.RegisterHandlersOfInstance(race_read_model)

print("### Part 2: Query Exiting data")
active_race = race_read_model.ActiveRaces()
print(active_race)

print("### Part 3: Create a new Race")
# from src.DungeonsDragons.Game.Race.Commands import (
#     CreateRace,
#     SetRaceDetails,
#     SetRaceAbilityScoreIncrease,
#     SetRaceAlignment
# )
# import uuid
# # We start by creating a race.
# race_id = uuid.uuid1()
# create_test_race = CreateRace(race_id)
# Dispatcher.SendCommand(create_test_race)
# set_test_race_details = SetRaceDetails(race_id, "Dwarf", "A Dwarf race")
# Dispatcher.SendCommand(set_test_race_details)
# set_test_ability_score = SetRaceAbilityScoreIncrease(race_id, [])
# Dispatcher.SendCommand(set_test_ability_score)
# set_test_race_alignment = SetRaceAlignment(race_id, 0, 0)
# Dispatcher.SendCommand(set_test_race_alignment)

# print(race_read_model.ActiveRaces())

