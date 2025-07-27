from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from faker import Faker
import time
from datetime import datetime, timedelta

fake = Faker()

# Schema Registry config
schema_registry_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

# Load Avro schema
with open("schema/chat_messages-value.avsc") as f:
    value_schema_str = f.read()

avro_serializer = AvroSerializer(schema_registry_client, value_schema_str)

producer_conf = {
    'bootstrap.servers': 'localhost:9092',
    'key.serializer': StringSerializer('utf_8'),
    'value.serializer': avro_serializer,
    'linger.ms': 50,                # internal buffering (50ms delay)
    'batch.size': 32768,            # batch size in bytes (32KB default)
    'queue.buffering.max.messages': 100000
}

producer = SerializingProducer(producer_conf)

BATCH_SIZE = 5000
BATCH_INTERVAL = 0.3  # 300 ms

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}] offset {msg.offset()}")

def generate_chat_message():
    now = int(datetime.utcnow().timestamp() * 1000)
    return {
        "sender_name": fake.name(),
        "message": fake.sentence(),
        "created_at": now,
        "updated_at": now
    }

try:
    while True:
        start_time = time.time()
        flush_time = datetime.now() + timedelta(seconds=BATCH_INTERVAL)
        count = 0

        while count < BATCH_SIZE and datetime.now() < flush_time:
            msg = generate_chat_message()
            producer.produce(
                topic='chat_messages',
                key=fake.uuid4(),
                value=msg,
                on_delivery=delivery_report
            )
            producer.poll(0)
            count = count + 1
            
        producer.flush()
        elapsed = time.time() - start_time
        print(f"Sent {count} messages in {elapsed:.2f}s")

except KeyboardInterrupt:
    print("Producer stopped")
    producer.flush()
