import pyshark
from classifier.utils.rabbitmq import RabbitMQ
import json

capture = pyshark.LiveCapture(interface='en0', bpf_filter='tcp port 443')

rabbitMQ = RabbitMQ("amqp://localhost:5672")
queue_name = "packets"


def print_callback(pkt):
    pkt = {
        "ip.src": str(pkt.ip.src),
        "tcp.dstport": str(pkt.tcp.dstport),
        "length": str(pkt.length),
        "tcp.srcport": str(pkt.tcp.srcport),
        "sniff_time": str(pkt.sniff_time)
    }

    rabbitMQ.publish(queue_name, json.dumps(pkt))


rabbitMQ.setup_queue(queue_name)
capture.apply_on_packets(print_callback)
