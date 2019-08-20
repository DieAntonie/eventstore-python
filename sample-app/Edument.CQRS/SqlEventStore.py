from IEventStore import IEventStore

class SqlEventStore(IEventStore):
    def __init__(self, hostname = 'localhost', username = 'postgres', password = 'masterkey', database = 'postgres'):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database = database

    def LoadEventsFor(self, id):
        import psycopg2
        connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        try:
            cur = connection.cursor()
            cur.execute(f"""
                SELECT [Type], [Body]
                FROM [dbo].[Events]
                WHERE [AggregateId] = {id}
                ORDER BY [SequenceNumber]
                """)

            for typeName, data in cur.fetchall() :
                yield self.DeserializeEvent(typeName, data)

        finally:
            connection.close()

    def DeserializeEvent(self, typeName, data):
        import json
        var ser = new XmlSerializer(Type.GetType(typeName))
        var ms = new MemoryStream(Encoding.UTF8.GetBytes(data))
        ms.Seek(0, SeekOrigin.Begin)
        return ser.Deserialize(ms)

    void SaveEventsFor<TAggregate>(Guid aggregateId, int eventsLoaded, ArrayList newEvents)
{
    using (var cmd = new SqlCommand())
    {
        // Query prelude.
        var queryText = new StringBuilder(512);
        queryText.AppendLine("BEGIN TRANSACTION;");
        queryText.AppendLine(
            @"IF NOT EXISTS(SELECT * FROM [dbo].[Aggregates] WHERE [Id] = @AggregateId)
                    INSERT INTO [dbo].[Aggregates] ([Id], [Type]) VALUES (@AggregateId, @AggregateType);");
        cmd.Parameters.AddWithValue("AggregateId", aggregateId);
        cmd.Parameters.AddWithValue("AggregateType", typeof(TAggregate).AssemblyQualifiedName);

        // Add saving of the events.
        cmd.Parameters.AddWithValue("CommitDateTime", DateTime.UtcNow);
        for (int i = 0; i < newEvents.Count; i++)
        {
            var e = newEvents[i];
            queryText.AppendFormat(
                @"INSERT INTO [dbo].[Events] ([AggregateId], [SequenceNumber], [Type], [Body], [Timestamp])
                    VALUES(@AggregateId, {0}, @Type{1}, @Body{1}, @CommitDateTime);",
                eventsLoaded + i, i);
            cmd.Parameters.AddWithValue("Type" + i.ToString(), e.GetType().AssemblyQualifiedName);
            cmd.Parameters.AddWithValue("Body" + i.ToString(), SerializeEvent(e));
        }

        // Add commit.
        queryText.Append("COMMIT;");

        // Execute the update.
        using (var con = new SqlConnection(connectionString))
        {
            con.Open();
            cmd.Connection = con;
            cmd.CommandText = queryText.ToString();
            cmd.CommandType = CommandType.Text;
            cmd.ExecuteNonQuery();
        }
    }
}

    string SerializeEvent(object obj)
{
    var ser = new XmlSerializer(obj.GetType());
    var ms = new MemoryStream();
    ser.Serialize(ms, obj);
    ms.Seek(0, SeekOrigin.Begin);
    return new StreamReader(ms).ReadToEnd();
}
}
}
