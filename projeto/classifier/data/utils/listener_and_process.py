import pyshark
import socket
import datetime
import numpy as np
import pickle
import os
import sys


capture = pyshark.LiveCapture(interface='en0', bpf_filter="tcp")

# bytes_counter by tcp service
tcp_services = dict()

# current host
current_host_name = socket.gethostbyname(socket.gethostname())

# num_arrived_pkts
num_arrived_pkts = 0

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "")


def arrived_pkt_callback(pkt):
    global current_host_name, num_arrived_pkts, tcp_services

    # number of packets arrived
    num_arrived_pkts += 1
    sys.stdout.write("\rArrived packets: {} | Ports: {}".format(num_arrived_pkts, str(list(tcp_services.keys()))))
    sys.stdout.flush()

    # verify if the tcp service has been already registered
    src_port = pkt.tcp.srcport
    dst_port = pkt.tcp.dstport

    # save the port to further update the tcp services dict

    if src_port in tcp_services.keys():
        # the packet belongs to one tcp service session
        service = tcp_services[src_port]
        port = src_port
    elif dst_port in tcp_services.keys():
        service = tcp_services[dst_port]
        port = dst_port
    else:
        port = dst_port
        # new tcp session, let's create it
        service = {
            "upload_bytes_counter": 0,
            "download_bytes_counter": 0,
            "last_timestamp": 0,
            "data_bytes_counter": np.array([[0, 0]])
        }

    # end verify

    # pkt source
    source = pkt.ip.src

    if service["last_timestamp"] == 0:
        if source == current_host_name:
            service["upload_bytes_counter"] += int(pkt.length)
        else:
            service["download_bytes_counter"] += int(pkt.length)

        service["last_timestamp"] = pkt.sniff_time
    else:
        # not first pkt
        timestamp_now = pkt.sniff_time
        timestamp_now = timestamp_now.replace(tzinfo=datetime.timezone.utc).timestamp()

        delta_time = ((datetime.datetime.utcfromtimestamp(int(timestamp_now))) - service["last_timestamp"]).total_seconds()

        if delta_time >= 1:
            # if passed more than one second, means we have to write n 0
            service["data_bytes_counter"] = np.append(service["data_bytes_counter"],
                                                      [[service["download_bytes_counter"],
                                                        service["upload_bytes_counter"]]], 0)

            for i in range(0, int(delta_time) - 1):
                service["data_bytes_counter"] = np.append(service["data_bytes_counter"], [[0, 0]], 0)

            service["upload_bytes_counter"] = 0
            service["download_bytes_counter"] = 0
        elif int(service["last_timestamp"].replace(tzinfo=datetime.timezone.utc).timestamp()) == int(
                timestamp_now):  # if it's the same timestamp, we have to increment
            source = pkt.ip.src

            if source == current_host_name:
                service["upload_bytes_counter"] += int(pkt.length)
            else:
                service["download_bytes_counter"] += int(pkt.length)

        service["last_timestamp"] = pkt.sniff_time

    # update tcp services
    tcp_services[port] = service


if __name__ == '__main__':
    try:
        capture.apply_on_packets(arrived_pkt_callback)
    except KeyboardInterrupt:
        ports = input("Which ports do you want to select (answer with CSV)?\n {}: ".format(list(tcp_services.keys())))

        ports = ports.replace(" ", "").split(",")

        for port in ports:
            prefix = input("\nPrefix name for the capture (port: {})?".format(port))

            with open(DATA_PATH + prefix + "_" + port + "_comm_record.bin", 'wb') as f:
                pickle.dump((tcp_services[port]["data_bytes_counter"]), f)
