from IEventStore import IEventStore
from datetime import datetime

class SqlEventStore(IEventStore):
    def __init__(self, host = 'localhost', user = 'postgres', password = 'masterkey', dbname = 'postgres'):
        self.host = host
        self.user = user
        self.password = password
        self.dbname = dbname

    def LoadEventsFor(self, id):
        import psycopg2
        with psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.dbname) as connection:
            db_cursor = connection.cursor()
            db_cursor.execute(f"""
                SELECT [Body]
                FROM [Events]
                WHERE [AggregateId] = {id}
                ORDER BY [SequenceNumber]
                """)

            for data in db_cursor.fetchall() :
                yield self.DeserializeEvent(data)

    def DeserializeEvent(self, data):
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
                module = __import__(module_name)
                # Get the class from the module
                class_ = getattr(module, class_name)
                # Use dictionary unpacking to initialize the object
                model_obj = class_(**json_obj)
            else:
                model_obj = json_obj
            return model_obj
        
        import json
        return json.loads(data, object_hook = json_to_model)

    def SaveEventsFor(self, aggregateId, eventsLoaded, newEvents):
        # Query prelude.
        queryText = f"""
            BEGIN TRANSACTION;
            IF NOT EXISTS(SELECT * FROM [Aggregates] WHERE [Id] = {aggregateId})
                INSERT INTO [Aggregates] ([Id]) VALUES ({aggregateId});
        """
        # Add saving of the events.
        CommitDateTime = datetime.now()
        for index, e in enumerate(newEvents):
            queryText += f"""
                INSERT INTO [Events] ([AggregateId], [SequenceNumber], [Body], [Timestamp])
                    VALUES('{aggregateId}', {eventsLoaded + index}, '{self.SerializeEvent(e)}', '{CommitDateTime}');
                """
        # Add commit.
        queryText += "COMMIT;"
        # Execute the update.
        import psycopg2
        with psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.dbname) as connection:
            db_cursor = connection.cursor()
            db_cursor.execute(queryText)

    def SerializeEvent(self, event):
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

        import json
        return json.dumps(event, default = model_to_json)
