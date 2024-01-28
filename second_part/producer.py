from random import choice

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


exchange = "hw_8_exchange"

# queue_name = "hw_8_queue"
# channel = connection.channel()
# channel.exchange_declare(exchange=exchange, exchange_type="direct")
# channel.queue_declare(queue=queue_name, durable=True)
# channel.queue_bind(exchange=exchange, queue=queue_name)

sms_queue_name = "sms_queue"
sms_channel = connection.channel()
sms_channel.exchange_declare(exchange=exchange, exchange_type="direct")
sms_channel.queue_declare(queue=sms_queue_name, durable=True)
sms_channel.queue_bind(exchange=exchange, queue=sms_queue_name)

email_queue_name = "email_queue"
email_channel = connection.channel()
email_channel.exchange_declare(exchange=exchange, exchange_type="direct")
email_channel.queue_declare(queue=email_queue_name, durable=True)
email_channel.queue_bind(exchange=exchange, queue=email_queue_name)


def create_contact():

    contact = Contact(fullname=fake.name(), 
                        email=fake.email(), 
                        address=fake.address(), 
                        phone_number=fake.phone_number(), 
                        preferred_shipping=choice(['SMS', 'email'])).save()
    return contact


def main():
    
    for _ in range(5):

        contact = create_contact()

        info = str(contact.id)

        match contact.preferred_shipping:

            case 'SMS':

                sms_channel.basic_publish(

                    exchange=exchange,
                    routing_key=sms_queue_name,
                    body=info.encode(),
                    properties=pika.BasicProperties(
                        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                    ),
                )

            case 'email':

                email_channel.basic_publish(

                    exchange=exchange,
                    routing_key=email_queue_name,
                    body=info.encode(),
                    properties=pika.BasicProperties(
                        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                    ),
                )

    connection.close()


if __name__ == "__main__":
    main()