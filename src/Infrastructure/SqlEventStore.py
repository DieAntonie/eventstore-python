from dataclasses import fields, is_dataclass
import uuid
from .IEvent import IEvent
from .IEventStore import IEventStore
from datetime import datetime
from enum import Enum
from typing import Sequence
from uuid import UUID


class SqlEventStore(IEventStore):
    def __init__(self, configuration: dict = { 'host':'localhost', 'user':'postgres', 'password':'postgres', 'dbname':'postgres'}):
        self.host = configuration['host']
        self.user = configuration['user']
        self.password = configuration['password']
        self.dbname = configuration['dbname']

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

    def LoadDomain(self, domain) -> Sequence[dict]:
        appliables = domain.Apply.registry.keys()
        domainType = domain.__class__.__name__
        eventTypes = [appliable.__name__ for appliable in appliables]
        import psycopg2
        with psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.dbname) as connection:
            db_cursor = connection.cursor()
            db_cursor.execute(f"""
                SELECT d.id, dr.revision, dr.structure
                FROM public.domain AS d
                JOIN public.domain_revision AS dr
                    ON d.id = dr.domain_id
                WHERE d.name = '{domainType}'
                ORDER BY dr.revision DESC
                LIMIT 1;
                """)
            domain_revisions = db_cursor.fetchall()
            if len(domain_revisions) == 0:
                domainId = uuid.uuid1()
                queryText = f"""
                    BEGIN TRANSACTION;

                    INSERT INTO public.domain (id, name)
                    SELECT
                        '{domainId}',
                        '{domainType}'
                    WHERE
                        NOT EXISTS (
                            SELECT id FROM public.domain WHERE id = '{domainId}'
                        );

                    INSERT INTO public.domain_revision (domain_id, structure)
                        VALUES(
                            '{domainId}',
                            '{{"events":["{'", "'.join(eventTypes)}"]}}');

                    COMMIT;
                    """
                db_cursor = connection.cursor()
                db_cursor.execute(queryText)
            else:
                revision = domain_revisions[0]
                response_revision = {
                    "id": revision[0],
                    "name": domainType,
                    "revision": revision[1],
                    "structure": revision[2]['events']
                }
                request_diff = list(set(eventTypes).difference(set(response_revision["structure"])))
                structure_diff = list(set(response_revision["structure"]).difference(set(eventTypes)))
                error_msg = []
                if (len(request_diff) > 0):
                    error_msg.append(f"Domain structure differs with {request_diff}")
                    print(error_msg)
                if (len(structure_diff) > 0):
                    error_msg.append(f"Persisted Domain structure differs with {structure_diff}")
                    print(error_msg)
            for appliable in appliables:
                if is_dataclass(appliable):
                    eventType = appliable.__name__
                    db_cursor.execute(f"""
                        SELECT e.id, er.revision, er.structure
                        FROM public.event AS e
                        JOIN public.event_revision AS er
                            ON e.id = er.event_id
                        WHERE e.name = '{eventType}'
                        ORDER BY er.revision DESC
                        LIMIT 1;
                        """)
                    event_revisions = db_cursor.fetchall()
                    if len(event_revisions) == 0:
                        eventId = uuid.uuid1()
                        queryText = f"""
                            BEGIN TRANSACTION;

                            INSERT INTO public.event (id, name)
                            SELECT
                                '{eventId}',
                                '{eventType}'
                            WHERE
                                NOT EXISTS (
                                    SELECT id FROM public.event WHERE id = '{eventId}'
                                );

                            INSERT INTO public.event_revision (event_id, structure)
                                VALUES(
                                    '{eventId}',
                                    '{{"properties":{{{', '.join([f'"{field.name}": "{field.type}"'.replace("'", "''") for field in fields(appliable)])}}}}}');

                            COMMIT;
                            """
                        print("queryText")
                        print(queryText)
                        db_cursor = connection.cursor()
                        db_cursor.execute(queryText)
                    else:
                        revision = event_revisions[0]
                        response_revision = {
                            "id": revision[0],
                            "name": eventType,
                            "revision": revision[1],
                            "structure": revision[2]['properties']
                        }
                        request_diff = list(set([(field.name,f"{field.type}") for field in fields(appliable)]).difference(set(list(response_revision["structure"].items()))))
                        structure_diff = list(set(list(response_revision["structure"].items())).difference(set([(field.name,f"{field.type}") for field in fields(appliable)])))
                        error_msg = []
                        if (len(request_diff) > 0):
                            error_msg.append(f"Event structure differs with {request_diff}")
                            print(error_msg)
                        if (len(structure_diff) > 0):
                            error_msg.append(f"Persisted Event structure differs with {structure_diff}")
                            print(error_msg)
