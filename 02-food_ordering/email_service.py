import json

from kafka_utils import Consumer
from settings import settings


consumer = Consumer(
    settings.ORDER_CONFIRMED_KAFKA_TOPIC, 
    bootstrap_servers=settings.KAFKA_BROKER
)

emails_sent_so_far = set()
print("Gonna start listening")
while True:
    for message in consumer:
        consumed_message = json.loads(message.value.decode())
        customer_email = consumed_message["customer_email"]
        print(f"Sending email to {customer_email} ")
        emails_sent_so_far.add(customer_email)
        print(f"So far emails sent to {len(emails_sent_so_far)} unique emails")