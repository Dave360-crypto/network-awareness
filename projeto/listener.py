import pyshark
import socket

capture = pyshark.LiveCapture(interface='en0', bpf_filter='tcp port 3355')


upload_counter = 0
upload_bytes = []
download_counter = 0
download_bytes = []


def print_callback(pkt):
    #print('Just arrived:', pkt)
    source = pkt.ip.src

    if source == socket.gethostbyname(socket.gethostname()):
        global upload_counter, upload_bytes
        upload_counter += 1
        upload_bytes.append(pkt.length)
    else:
        global download_counter, download_bytes
        download_counter += 1
        download_bytes.append(pkt.length)
    print(upload_bytes)

capture.apply_on_packets(print_callback)
