import json

from kafka_utils import Consumer
from settings import settings


consumer = Consumer(
    settings.ORDER_CONFIRMED_KAFKA_TOPIC, 
    bootstrap_servers=settings.KAFKA_BROKER
)

total_orders_count = 0
total_revenue = 0
print("Gonna start listening")
while True:
    for message in consumer:
        print("Updating analytics..")
        consumed_message = json.loads(message.value.decode())
        total_cost = float(consumed_message["total_cost"])
        total_orders_count += 1
        total_revenue += total_cost
        print(f"Orders so far today: {total_orders_count}")
        print(f"Revenue so far today: {total_revenue}")