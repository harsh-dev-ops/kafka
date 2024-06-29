import time
from kafka_utils import Producer
from settings import settings
from utils import json_encoder

producer = Producer(bootstrap_servers=settings.KAFKA_BROKER)

for i in range(0,10):
    data = {
        'id': i +1,
        'user_id': i*10,
        'total_cost': i +100,
        "items": [
            'burger',
            'Sandwich',
            'Pizza'
        ]
    }
    # print("Sending:", data)
    time.sleep(1)
    producer.send(settings.ORDER_KAFKA_TOPIC, json_encoder(data))