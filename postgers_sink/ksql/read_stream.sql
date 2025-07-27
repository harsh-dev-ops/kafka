SELECT sender_name, 
    message, 
    TIMESTAMPTOSTRING(created_at, 'yyyy-MM-dd HH:mm:ss') AS created_time, 
    TIMESTAMPTOSTRING(updated_at, 'yyyy-MM-dd HH:mm:ss') AS updated_at
FROM chat_messages_stream
EMIT CHANGES;