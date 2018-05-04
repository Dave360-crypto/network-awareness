import pyshark

capture = pyshark.LiveCapture(interface='en0', bpf_filter='tcp port 3355')

def print_callback(pkt):
    print('Just arrived:', pkt)

capture.apply_on_packets(print_callback)
