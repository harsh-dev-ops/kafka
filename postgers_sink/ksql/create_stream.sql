DROP STREAM IF EXISTS chat_messages_stream;

CREATE STREAM IF NOT EXISTS chat_messages_stream (
    sender_name VARCHAR,
    message VARCHAR,
  created_at BIGINT,
updated_at BIGINT
) WITH (
    KAFKA_TOPIC = 'chat_messages',
    VALUE_FORMAT = 'AVRO',
    VALUE_SCHEMA_ID = 1
);