import os
import pickle
from classifier.utils.rabbitmq import RabbitMQ
import json


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "classifier/data/")

with open(DATA_PATH + "bin/live_data.bin", 'rb') as f:
    packets = pickle.load(f)


rabbitMQ = RabbitMQ("amqp://localhost:5672")
queue_name = "packets"

rabbitMQ.setup_queue(queue_name)

for pkt in packets:
    if "tcp.dstport" not in pkt:
        pkt["tcp.dstport"] = 443  # example YouTube

    rabbitMQ.publish(queue_name, json.dumps(pkt))

print("All packets emitted!")
