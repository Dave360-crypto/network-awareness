#------------------------------------LISTENER YOUTUBE------------------------------------------------
import pyshark
import socket
import datetime

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
    capture.apply_on_packets(print_callback, timeout=30)
except Exception as e:
    last_timestamp = 0
    print("Timeout")

    for index, pkt in packets.items():
        source = pkt.ip.src
        if index==0:
            if source == socket.gethostbyname(socket.gethostname()):
                upload_counter += 1
                upload_bytes_counter += int(pkt.length)
                # contar os portos de origem
                if pkt.tcp.srcport in upload_ports:
                    upload_ports[pkt.tcp.srcport] += 1
                else:
                    upload_ports[pkt.tcp.srcport] = 1

            else:
                download_counter += 1
                download_bytes_counter += int(pkt.length)
                # contar os portos de origem
                if pkt.tcp.srcport in download_ports:
                    download_ports[pkt.tcp.srcport] += 1
                else:
                    download_ports[pkt.tcp.srcport] = 1

            last_timestamp = packets[index].sniff_time
            continue

        timestamp_now = packets[index].sniff_time
        timestamp_now = timestamp_now.replace(tzinfo=datetime.timezone.utc).timestamp()

        delta_time = ((datetime.datetime.utcfromtimestamp(int(timestamp_now))) - last_timestamp).total_seconds()

        if delta_time >= 1: # if passed more than one second, means we have to write n 0
            upload_bytes.append(upload_bytes_counter)
            download_bytes.append(download_bytes_counter)

            for i in range(0, int(delta_time)-1):
                upload_bytes.append(0)
                download_bytes.append(0)

            upload_bytes_counter = 0
            download_bytes_counter = 0
        elif int(last_timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()) == int(timestamp_now): # if it's the same timestamp, we have to increment
            source = pkt.ip.src

            if source == socket.gethostbyname(socket.gethostname()):
                upload_counter += 1
                upload_bytes_counter += int(pkt.length)
                # contar os portos de origem
                if pkt.tcp.srcport in upload_ports:
                    upload_ports[pkt.tcp.srcport] += 1
                else:
                    upload_ports[pkt.tcp.srcport] = 1

            else:
                download_counter += 1
                download_bytes_counter += int(pkt.length)
                # contar os portos de origem
                if pkt.tcp.srcport in download_ports:
                    download_ports[pkt.tcp.srcport] += 1
                else:
                    download_ports[pkt.tcp.srcport] = 1

        last_timestamp = packets[index].sniff_time


#------------------------------------PROCESS DATA------------------------------------------------

download_upload_bytes = " "

lines_download = len(download_bytes)
lines_upload = len(upload_bytes)

if lines_download < lines_upload:
    size_bytes = lines_download
else:
    size_bytes = lines_upload

print("down:", download_bytes)
print("up:", upload_bytes)

for i in range(0, size_bytes):
    download_upload_bytes += str(download_bytes[i]) + " " + str(upload_bytes[i]) + "\n"

print(download_upload_bytes)
