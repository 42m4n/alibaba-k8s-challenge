#!/usr/bin/python3
import pika
import os
import random

# Connect to RabbitMQ
rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
docker_queue = os.environ.get('RABBITMQ_QUEUE', 'ticket-queue')
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))

channel = connection.channel()

# Declare queue
channel.queue_declare(queue=docker_queue)

ticket_number = random.randint(1000, 9999)
message_body = f'AliBaba ticket number {ticket_number}'
channel.basic_publish(exchange='',
                      routing_key=docker_queue,
                      body=message_body)
print(f" [x] Sent massege: {message_body}")

connection.close()
