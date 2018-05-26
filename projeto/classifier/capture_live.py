#------------------------------------LISTENER YOUTUBE------------------------------------------------
import numpy as np
import pyshark
import socket
import datetime
import pickle, os

capture = pyshark.LiveCapture(interface='en0', bpf_filter='tcp port 443', )

upload_counter = 0
upload_bytes_counter = 0
download_bytes_counter = 0
upload_ports = {}
download_counter = 0
download_ports = {}
download_ports_counter = 0
upload_ports_counter = 0
packets = {}
upload_bytes = []
download_bytes = []

index = 0
count = 0


def print_callback(pkt):
    global index
    global count
    packets[index] = pkt
    index += 1

try:
    capture.apply_on_packets(print_callback)

except KeyboardInterrupt:
    DATA_PATH = os.path.join(os.path.dirname(__file__), "data/")
    with open(DATA_PATH + "bin/live_data.bin", 'wb') as f:
        pickle.dump(packets, f)
    f.close()
