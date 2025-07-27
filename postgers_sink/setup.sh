docker compose up -d

sleep 5

docker compose exec -T postgres psql -U postgres -d postgres < sql/init_db.sql

sleep 60

docker exec -it broker kafka-topics --create \
   --topic chat_messages \
   --partitions 1 \
   --replication-factor 1 \
   --bootstrap-server broker:29092

sleep 1

curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
     --data @<(jq -n --arg schema "$(cat schema/chat_messages-value.avsc)" '{schema: $schema}') \
      http://localhost:8081/subjects/chat_messages-value/versions


sleep 5

curl -X POST -H "Content-Type: application/json" \
     --data @"connectors/jdbc-chat-sink.json" \
     http://localhost:8083/connectors