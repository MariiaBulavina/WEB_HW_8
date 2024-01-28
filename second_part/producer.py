import json
from datetime import datetime
import faker

import pika

from models import Contact

fake = faker.Faker()

credentials = pika.PlainCredentials("sqasnxyg", "YKyUq_5sEQnPdvfdq-LPnH0nxsYcdvqr")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="albatross-01.rmq.cloudamqp.com",
        port=5672,
        credentials=credentials,
        virtual_host="sqasnxyg",
    )
)

channel = connection.channel()

exchange = "hw_8_exchange"
queue_name = "hw_8_queue"

channel.exchange_declare(exchange=exchange, exchange_type="direct")
channel.queue_declare(queue=queue_name, durable=True)
channel.queue_bind(exchange=exchange, queue=queue_name)


def create_contacts(nums: int):
    for _ in range(nums):
        contact = Contact(fullname=fake.name(), email=fake.email(), address=fake.address()).save()

        channel.basic_publish(

            exchange=exchange,
            routing_key=queue_name,
            body=str(contact.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

    connection.close()


if __name__ == "__main__":
    create_contacts(50)