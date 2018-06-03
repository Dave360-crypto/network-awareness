import pyshark
import socket
import datetime
import numpy as np
import pickle
import os, sys

print("Mining: tcp port 3355")
print("HTTPS: tcp port 443")
print("HTTP: tcp port 80")
print("Browsing: tcp port 443 or 80")

cap_filter = input("Filter:")

capture = pyshark.LiveCapture(interface='en0', bpf_filter=cap_filter)

# record into list
comm_up_down = np.array([[0, 0]])

# bytes counter for upload
upload_bytes_counter = 0

# bytes counter for download
download_bytes_counter = 0

# upload ports counter
upload_ports = {}
upload_ports_counter = 0

# download ports counter
download_ports = {}
download_ports_counter = 0

# timestamp
last_timestamp = 0

# current host
current_host_name = socket.gethostbyname(socket.gethostname())


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "")

# count
num_arrived_pkts = 0


def arrived_pkt_callback(pkt):
    global last_timestamp, comm_up_down, upload_bytes_counter, download_bytes_counter, upload_ports,\
        upload_ports_counter, download_ports, download_ports_counter, current_host_name, num_arrived_pkts

    num_arrived_pkts += 1
    sys.stdout.write("\rArrived packets: {}".format(num_arrived_pkts))
    sys.stdout.flush()

    # pkt source
    source = pkt.ip.src

    if last_timestamp == 0:
        if source == current_host_name:
            upload_bytes_counter += int(pkt.length)

            # contar os portos de origem
            if str(pkt.tcp.srcport) in upload_ports:
                upload_ports[str(pkt.tcp.srcport)] += 1
            else:
                upload_ports[str(pkt.tcp.srcport)] = 1

        else:
            download_bytes_counter += int(pkt.length)

            # contar os portos de origem
            if str(pkt.tcp.srcport) in download_ports:
                download_ports[str(pkt.tcp.srcport)] += 1
            else:
                download_ports[str(pkt.tcp.srcport)] = 1

        last_timestamp = pkt.sniff_time
    else:
        # not first pkt
        timestamp_now = pkt.sniff_time
        timestamp_now = timestamp_now.replace(tzinfo=datetime.timezone.utc).timestamp()

        delta_time = ((datetime.datetime.utcfromtimestamp(int(timestamp_now))) - last_timestamp).total_seconds()

        if delta_time >= 1:
            # if passed more than one second, means we have to write n 0
            comm_up_down = np.append(comm_up_down, [[download_bytes_counter, upload_bytes_counter]], 0)

            for i in range(0, int(delta_time) - 1):
                comm_up_down = np.append(comm_up_down, [[0, 0]], 0)

            upload_bytes_counter = 0
            download_bytes_counter = 0
        elif int(last_timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()) == int(
                timestamp_now):  # if it's the same timestamp, we have to increment
            source = pkt.ip.src

            if source == socket.gethostbyname(socket.gethostname()):
                upload_bytes_counter += int(pkt.length)

                # contar os portos de origem
                if str(pkt.tcp.srcport) in upload_ports:
                    upload_ports[str(pkt.tcp.srcport)] += 1
                else:
                    upload_ports[str(pkt.tcp.srcport)] = 1

            else:
                download_bytes_counter += int(pkt.length)

                # contar os portos de origem
                if str(pkt.tcp.srcport) in download_ports:
                    download_ports[str(pkt.tcp.srcport)] += 1
                else:
                    download_ports[str(pkt.tcp.srcport)] = 1

        last_timestamp = pkt.sniff_time


if __name__ == '__main__':
    prefix = input("Prefix name for the capture?")

    try:
        capture.apply_on_packets(arrived_pkt_callback)
    except KeyboardInterrupt:
        # saving comm_up_down, upload_ports and download_ports

        with open(DATA_PATH + prefix + "_comm_record.bin", 'wb') as f:
            pickle.dump((comm_up_down, upload_ports, download_ports), f)
