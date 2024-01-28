import pika

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

sms_channel = connection.channel()
sms_queue_name = "sms_queue"
sms_channel.queue_declare(queue=sms_queue_name, durable=True)


def callback(ch, method, properties, body):

    message = body.decode()

    contact = Contact.objects(id=message)

    sending_result = send_message()

    if sending_result:
        contact.update(set__sent=True)

    ch.basic_ack(delivery_tag=method.delivery_tag)


sms_channel.basic_qos(prefetch_count=1)
sms_channel.basic_consume(queue=sms_queue_name, on_message_callback=callback)


def send_message():
    return True


if __name__ == '__main__':
    sms_channel.start_consuming()
