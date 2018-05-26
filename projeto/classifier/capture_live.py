import pyshark
import pickle, os

capture = pyshark.LiveCapture(interface='en0', bpf_filter='tcp port 443', )

packets = {}

index = 0


def print_callback(pkt):
    global index
    packets[index] = pkt
    index += 1

try:
    capture.apply_on_packets(print_callback)

except KeyboardInterrupt:
    DATA_PATH = os.path.join(os.path.dirname(__file__), "data/")

    with open(DATA_PATH + "bin/live_data.bin", 'wb') as f:
        pickle.dump(packets, f)

    f.close()
