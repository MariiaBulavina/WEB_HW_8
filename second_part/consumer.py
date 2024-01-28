import json
import os
import sys
import time

import pika
from bson import json_util

from models import Contact


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
queue_name = "hw_8_queue"
channel.queue_declare(queue=queue_name, durable=True)


def callback(ch, method, properties, body):

    message = body.decode()

    contact = Contact.objects(id=message)

    sending_result = send_message()

    if sending_result:
        contact.update(set__sent=True)

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=callback)



def send_message():
    return True


if __name__ == '__main__':
    channel.start_consuming()
