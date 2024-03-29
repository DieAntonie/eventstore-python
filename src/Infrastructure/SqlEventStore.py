from .IEvent import IEvent
from .IEventStore import IEventStore
from datetime import datetime
from enum import Enum
from typing import Sequence
from uuid import UUID


class SqlEventStore(IEventStore):
    def __init__(self, host='localhost', user='postgres', password='postgres', dbname='postgres'):
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname

    def LoadEventsByType(self, eventTypes: Sequence[str]) -> Sequence[IEvent]:
        """
        Loads all events of the specified types.
        """
        import psycopg2
        with psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.dbname) as connection:
            db_cursor = connection.cursor()
            db_cursor.execute(f"""
                SELECT body
                FROM public.events
                WHERE type in ({','.join([f"'{eventType}'" for eventType in eventTypes])})
                ORDER BY timestamp, sequence_number;
                """)

            for data in db_cursor.fetchall():
                yield self.DeserializeEvent(data)

    def LoadEventsForAggregate(self, id: UUID) -> Sequence[IEvent]:
        """
        Loads the collection of events for the specified aggregate key.
        """
        import psycopg2
        with psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.dbname) as connection:
            db_cursor = connection.cursor()
            db_cursor.execute(f"""
                SELECT body
                FROM public.events
                WHERE aggregate_id = '{id}'
                ORDER BY sequence_number;
                """)

            for data in db_cursor.fetchall():
                yield self.DeserializeEvent(data)

    def DeserializeEvent(self, data) -> IEvent:
        """
        Deserializes the event `data` into an instance of an Event.
        """
        def json_to_model(json_obj: dict) -> IEvent:
            """
            Function that takes in a dict and returns a custom object associated with the dict.
            This function makes use of the "__module__" and "__class__" metadata in the dictionary
            to know which object type to create.
            """
            if "__class__" in json_obj:
                # Pop ensures we remove metadata from the dict to leave only the instance arguments
                class_name = json_obj.pop("__class__")
                # Get the module name from the dict and import it
                module_name = json_obj.pop("__module__")
                # We use the built in __import__ function since the module name is not yet known at runtime
                module = __import__(module_name, fromlist=[module_name])
                # Get the class from the module
                class_ = getattr(module, class_name)
                # Use dictionary unpacking to initialize the object
                model_obj = class_(**json_obj)
            elif"__enum__" in json_obj:
                # Pop ensures we remove metadata from the dict to leave only the instance arguments
                enum_name = json_obj.pop("__enum__")
                # Get the module name from the dict and import it
                module_name = json_obj.pop("__module__")
                # We use the built in __import__ function since the module name is not yet known at runtime
                module = __import__(module_name, fromlist=[module_name])
                # Get the class from the module
                enum_ = getattr(module, enum_name)
                # Use dictionary unpacking to initialize the object
                model_obj = enum_(**json_obj)
            else:
                model_obj = json_obj
            return model_obj

        import json
        # TODO: This list casting thing doesn't seem like it's going to work forever...
        return json.loads(json.dumps(list(data)[0]), object_hook=json_to_model)

    def SaveEvents(self, aggregateType: str, eventsLoaded: int, newEvents: Sequence[IEvent]) -> None:
        """
        Stores the collection of appended events for the aggregate key.
        """
        # Query prelude.
        # Add saving of the events.
        index = 0 
        queryText = "BEGIN TRANSACTION;"
        for event in newEvents:
            queryText += f"""
                INSERT INTO public.aggregates (id, type)
                SELECT
                    '{event.Id}',
                    '{aggregateType}'
                WHERE
                    NOT EXISTS (
                        SELECT id FROM public.aggregates WHERE id = '{event.Id}'
                    );
                    
                INSERT INTO public.events (aggregate_id, sequence_number, type, body, timestamp)
                    VALUES(
                        '{event.Id}',
                        {eventsLoaded + index},
                        '{event.__class__.__name__}',
                        '{self.SerializeEvent(event)}',
                        '{datetime.utcnow()}');
                """
            index += 1
        # Add commit.
        queryText += "COMMIT;"
        # Execute the update.
        import psycopg2
        with psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.dbname) as connection:
            db_cursor = connection.cursor()
            db_cursor.execute(queryText)

    def SerializeEvent(self, event: IEvent) -> str:
        """
        Serializes the `event` to deserializable JSON state.
        """
        import json

        class UUIDEncoder(json.JSONEncoder):
            """
            uuid encoder for correctly casting uuid values.
            """

            def default(self, obj) -> dict:
                if isinstance(obj, UUID):
                    # if the obj is uuid, we simply return the value of uuid
                    return obj.hex
                elif isinstance(obj, Enum):
                    # if the obj is uuid, we simply return the value of uuid
                    return enum_to_json(obj)
                return model_to_json(obj)

        def enum_to_json(enum_obj) -> dict:
            """
            A function takes in a custom object and returns a dictionary representation of the object.
            This dict representation includes meta data such as the object's module and class names.
            """
            #  Populate the dictionary with object meta data
            json_obj = {
                "__enum__": str(enum_obj),
                "__module__": enum_obj.__module__
            }
            #  Populate the dictionary with object properties
            return json_obj

        def model_to_json(model_obj) -> dict:
            """
            A function takes in a custom object and returns a dictionary representation of the object.
            This dict representation includes meta data such as the object's module and class names.
            """
            #  Populate the dictionary with object meta data
            json_obj = {
                "__class__": model_obj.__class__.__name__,
                "__module__": model_obj.__module__
            }
            #  Populate the dictionary with object properties
            json_obj.update(model_obj.__dict__)
            return json_obj

        return json.dumps(event, cls=UUIDEncoder)
