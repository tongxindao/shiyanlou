#!/usr/bin/env python
import pika
import sys


connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            "localhost"))
channel = connection.channel()

channel.exchange_declare(exchange="logs",
        type="fanout")

message = " ".join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(exchange="logs",
        routing_key="",
        body=message)

print(" [x] Sent 'Hello World!'")

connection.close()
