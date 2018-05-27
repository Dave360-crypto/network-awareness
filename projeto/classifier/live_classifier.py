import numpy as np
import socket
import os, pickle
import json
import datetime

upload_counter = 0
upload_bytes_counter = 0

download_counter = 0
download_bytes_counter = 0

upload_ports = {}
download_ports = {}

download_ports_counter = 0
upload_ports_counter = 0
upload_bytes = []
download_bytes = []

index = 0
count = 0

last_timestamp = 0

current_host_name = socket.gethostbyname(socket.gethostname())


def callback(channel, method_frame, header_frame, body):
    global index, last_timestamp, upload_counter, upload_bytes_counter, download_counter, download_bytes_counter, \
        upload_ports, download_ports, current_host_name

    pkt = json.dumps(body.decode())

    source = pkt["ip.src"]

    if index == 0:
        if source == current_host_name:
            upload_counter += 1
            upload_bytes_counter += int(pkt["length"])
            # contar os portos de origem
            if pkt["tcp.srcport"] in upload_ports:
                upload_ports[pkt["tcp.srcport"]] += 1
            else:
                upload_ports[pkt["tcp.srcport"]] = 1

        else:
            download_counter += 1
            download_bytes_counter += int(pkt["length"])
            # contar os portos de origem
            if pkt["tcp.srcport"] in download_ports:
                download_ports[pkt["tcp.srcport"]] += 1
            else:
                download_ports[pkt["tcp.srcport"]] = 1

        last_timestamp = datetime.datetime.strptime(pkt["sniff_time"], "%Y-%m-%d %H:%M:%S.%f")
    else:
        # index != 0
        timestamp_now = datetime.datetime.strptime(pkt["sniff_time"], "%Y-%m-%d %H:%M:%S.%f")
        timestamp_now = timestamp_now.replace(tzinfo=datetime.timezone.utc).timestamp()

        delta_time = ((datetime.datetime.utcfromtimestamp(int(timestamp_now))) - last_timestamp).total_seconds()

        if delta_time >= 1:  # if passed more than one second, means we have to write n 0
            upload_bytes.append(upload_bytes_counter)
            download_bytes.append(download_bytes_counter)

            for i in range(0, int(delta_time) - 1):
                upload_bytes.append(0)
                download_bytes.append(0)

            upload_bytes_counter = 0
            download_bytes_counter = 0

        elif int(last_timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()) == int(
                timestamp_now):  # if it's the same timestamp, we have to increment
            source = pkt["ip.src"]

            if source == current_host_name:
                upload_counter += 1
                upload_bytes_counter += int(pkt["length"])
                # contar os portos de origem
                if pkt["tcp.srcport"] in upload_ports:
                    upload_ports[pkt["tcp.srcport"]] += 1
                else:
                    upload_ports[pkt["tcp.srcport"]] = 1

            else:
                download_counter += 1
                download_bytes_counter += int(pkt["length"])
                # contar os portos de origem
                if pkt["tcp.srcport"] in download_ports:
                    download_ports[pkt["tcp.srcport"]] += 1
                else:
                    download_ports[pkt["tcp.srcport"]] = 1

        last_timestamp = datetime.datetime.strptime(pkt["sniff_time"], "%Y-%m-%d %H:%M:%S.%f")

    # ack and inc index

    index += 1

    # make download upload bytes array


    """
    when the size_bytes get's some value it will discard  old bytes and only X most recent bytes will be take in account
    """

    

    channel.basic_ack(delivery_tag=method_frame.delivery_tag)




# ------------------------------------PROCESS DATA------------------------------------------------

download_upload_bytes = []

lines_download = len(download_bytes)
lines_upload = len(upload_bytes)

if lines_download < lines_upload:
    size_bytes = lines_download
else:
    size_bytes = lines_upload

for i in range(0, size_bytes):
    download_upload_bytes.append([download_bytes[i], upload_bytes[i]])

unknown_data = np.array(download_upload_bytes).reshape(size_bytes, 2)


if __name__ == '__main__':
    pass
