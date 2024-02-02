import pika
import json
import time
import os

# Connect to RabbitMQ
rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
docker_queue = os.environ.get('RABBITMQ_QUEUE', 'ticket-queue')
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
channel = connection.channel()

# Function will be applied then message received
def callback(ch, method, properties, body):
    print("processing...")
    if properties.content_type == 'application/json':
        d = json.loads(body.decode())
        print(" [x] Received %r" % d)
    else:
        print(" [x] Received %r" % body.decode())
    time.sleep(5)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.queue_declare(queue=docker_queue)

channel.basic_consume(queue=docker_queue,
                      auto_ack=False,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
