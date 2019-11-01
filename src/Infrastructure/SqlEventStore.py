from .IEventStore import IEventStore
from datetime import datetime
from uuid import UUID
from enum import Enum


class SqlEventStore(IEventStore):
    def __init__(self, host='localhost', user='postgres', password='masterkey', dbname='postgres'):
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname

    def LoadEventsFor(self, id):
        """
        Loads the collection of events for the specified aggregate key.
        """
        import psycopg2
        with psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.dbname) as connection:
            db_cursor = connection.cursor()
            db_cursor.execute(f"""
                SELECT "Body"
                FROM public."Events"
                WHERE "AggregateId" = '{id}'
                ORDER BY "SequenceNumber"
                """)

            for data in db_cursor.fetchall():
                yield self.DeserializeEvent(data)

    def DeserializeEvent(self, data):
        """
        Deserializes the event `data` into an instance of an Event.
        """
        def json_to_model(json_obj):
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
            if "__enum__" in json_obj:
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

    def SaveEventsFor(self, aggregateId, aggregateType, eventsLoaded, newEvents):
        """
        Stores the collection of appended events for the aggregate key.
        """
        # Query prelude.
        queryText = f"""
            BEGIN TRANSACTION;
            INSERT INTO public."Aggregates"
                ("Id", "Type")
            SELECT  '{aggregateId}',
                    '{aggregateType}'
            WHERE
                NOT EXISTS (
                    SELECT "Id" FROM public."Aggregates" WHERE "Id" = '{aggregateId}'
                );
        """
        # Add saving of the events.
        CommitDateTime = datetime.now()
        for index, event in enumerate(newEvents):
            queryText += f"""
                INSERT INTO public."Events" ("AggregateId", "SequenceNumber", "Type", "Body", "Timestamp")
                    VALUES('{aggregateId}', {eventsLoaded + index}, '{event.__class__.__name__}', '{self.SerializeEvent(event)}', '{CommitDateTime}');
                """
        # Add commit.
        queryText += "COMMIT;"
        # Execute the update.
        import psycopg2
        with psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.dbname) as connection:
            db_cursor = connection.cursor()
            db_cursor.execute(queryText)

    def SerializeEvent(self, event):
        """
        Serializes the `event` to deserializable JSON state.
        """
        import json

        class UUIDEncoder(json.JSONEncoder):
            """
            uuid encoder for correctly casting uuid values.
            """

            def default(self, obj):
                if isinstance(obj, UUID):
                    # if the obj is uuid, we simply return the value of uuid
                    return obj.hex
                elif isinstance(obj, Enum):
                    # if the obj is uuid, we simply return the value of uuid
                    return enum_to_json(obj)
                return model_to_json(obj)

        def enum_to_json(enum_obj):
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

        def model_to_json(model_obj):
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
