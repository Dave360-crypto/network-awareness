import pyshark
import pickle
import os

capture = pyshark.LiveCapture(interface='en0', bpf_filter='tcp port 443', )

packets = {}

index = 0


def print_callback(pkt):
    global index

    pkt = {
        "ip.src": str(pkt.ip.src),
        "tcp.dstport": str(pkt.tcp.dstport),
        "length": str(pkt.length),
        "tcp.srcport": str(pkt.tcp.srcport),
        "sniff_time": pkt.sniff_time
    }

    packets[index] = pkt
    index += 1

try:
    capture.apply_on_packets(print_callback)
except KeyboardInterrupt:
    DATA_PATH = os.path.join(os.path.dirname(__file__), "data/")

    with open(DATA_PATH + "bin/live_data.bin", 'wb') as f:
        pickle.dump(packets, f)

    f.close()
