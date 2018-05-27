#!/usr/bin/python3

import pika


class RabbitMQ:
    def __init__(self, amqp_url, queue_names=[]):
        params = pika.URLParameters(amqp_url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_size=0, prefetch_count=1)
        self.channel.confirm_delivery()

        # Declare queues
        for queue_name in queue_names:
            self.setup_queue(queue_name)

    def publish(self, queue_name, message):
        return self.channel.basic_publish(exchange="",
                                          routing_key=queue_name,
                                          body=message,
                                          properties=pika.BasicProperties(
                                              content_type="application/json",
                                              delivery_mode=2),
                                          mandatory=True)

    def setup_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name, durable=True)
