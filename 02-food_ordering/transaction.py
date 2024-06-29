import json
from settings import settings
from utils import json_decoder, json_encoder

from kafka_utils import Producer, Consumer

producer = Producer(bootstrap_servers=settings.KAFKA_BROKER)
consumer = Consumer(settings.ORDER_KAFKA_TOPIC, bootstrap_servers=settings.KAFKA_BROKER)

for message in consumer:
    print("Ongoing Transaction")
    consumed_message = json_decoder(message.value.decode())
    print("Order Details:", consumed_message)
    user_id = consumed_message['user_id']
    order_id = consumed_message['id']
    cost = consumed_message['total_cost']
    
    data = {
            "order_id": order_id,
            "customer_id": user_id,
            "customer_email": f"{user_id}@gmail.com",
            "total_cost": cost
        }
    
    producer.send(settings.ORDER_CONFIRMED_KAFKA_TOPIC, json_encoder(data))