# Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/harsh-dev-ops/kafka.git
   ```

2. **Change directory**:
   ```bash
   cd postgers_sink
   ```
   
3. **Start the infrastructure**:
   ```bash
   docker compose up -d
   ```

4. **JDBC connector download (optional, commands already included in docker compose)**
   1. Visit: https://www.confluent.io/hub/confluentinc/kafka-connect-jdbc
   2. Download the latest version (e.g., confluentinc-kafka-connect-jdbc-10.8.4.zip).
   3. Extract it into your connectors folder:
   ```bash
   mkdir -p connectors/jdbc-connector
   unzip confluentinc-kafka-connect-jdbc-10.8.4.zip -d connectors/jdbc-connector
   ```

5. **Initialize PostgreSQL**:
   ```bash
   docker compose exec -T postgres psql -U postgres -d postgres < sql/init_db.sql
   ```

<!-- 4. **Download PostgreSQL JDBC driver**:
   ```bash
   mkdir -p postgres-driver
   wget https://jdbc.postgresql.org/download/postgresql-42.7.7.jar -O postgres-driver/postgresql-42.7.7.jar
   ``` -->

6. **Create Kakfa topic**
   ```bash
   docker exec -it broker kafka-topics --create \
   --topic chat_messages \
   --partitions 1 \
   --replication-factor 1 \
   --bootstrap-server broker:29092
   ```

7. **Register your kafka topic schema**
   ```bash
   curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
     --data @<(jq -n --arg schema "$(cat schema/chat_messages-value.avsc)" '{schema: $schema}') \
      http://localhost:8081/subjects/chat_messages-value/versions
   ```

8. **Deploy Kafka Connect connector** (wait for Connect to start):
   ```bash
   curl -X POST -H "Content-Type: application/json" \
     --data @"connectors/jdbc-chat-sink.json" \
     http://localhost:8083/connectors
   ```
9. **Create new virtual environment**:
   ```bash
   python3 -m venv venv
   ```

10. **Activate the venv**
    ```bash
    source venv/bin/activate
    ```

11. **Install the dependencies**
   ```sh
   pip install -r requirements.txt
   ```

12. **Run the producer** (in a new terminal):
   ```bash
   python producer.py
   ```

## Key Features:

1. **Batch Processing**:
   - Messages are batched every 100ms (`flush.interval.ms`)
   - OR when 1000 messages are collected (`batch.size` and `flush.size`)

2. **Data Generation**:
   - Uses Faker to generate realistic chat messages
   - Each message has all required fields for PostgreSQL table

3. **Error Handling**:
   - Retry mechanism with backoff
   - Delivery reports for producer

4. **Monitoring**:
   - Consumer shows messages in real-time
   - You can verify data in PostgreSQL:
     ```bash
     docker exec -it postgres psql -U postgres -d postgres -c "SELECT COUNT(*) FROM ChatMessages;"
     ```
