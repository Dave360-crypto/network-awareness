import socket
import json
import datetime
import numpy as np
import sys
from classifier.utils.rabbitmq import RabbitMQ
from classifier.utils.classify import breakData, extractFeatures, extractFeaturesSilence, extractFeaturesWavelet
from classifier.distances.classify_distances import classify_distances


rabbitMQ = RabbitMQ("amqp://localhost:5672")

# Bytes counter (download and upload)

upload_bytes_counter = 0
download_bytes_counter = 0

unknown_data_bytes_counter = np.array([[0, 0]])

# Ports counter (upload and download)

upload_ports = {}
download_ports = {}

download_ports_counter = 0
upload_ports_counter = 0

# [END] ports counter (upload and download)

index = 0
count = 0

last_timestamp = 0

current_host_name = socket.gethostbyname(socket.gethostname())


def callback(channel, method_frame, header_frame, body):
    global index, last_timestamp, upload_bytes_counter, download_bytes_counter, unknown_data_bytes_counter, \
        upload_ports, download_ports, current_host_name

    pkt = json.loads(body.decode())

    source = pkt["ip.src"]

    if index == 0:
        if source == current_host_name:
            upload_bytes_counter += int(pkt["length"])

            # contar os portos de origem
            if pkt["tcp.srcport"] in upload_ports:
                upload_ports[pkt["tcp.srcport"]] += 1
            else:
                upload_ports[pkt["tcp.srcport"]] = 1

        else:
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
            unknown_data_bytes_counter = np.append(unknown_data_bytes_counter, [[download_bytes_counter,
                                                                                 upload_bytes_counter]], 0)

            for i in range(0, int(delta_time) - 1):
                unknown_data_bytes_counter = np.append(unknown_data_bytes_counter, [[0, 0]], 0)

            upload_bytes_counter = 0
            download_bytes_counter = 0

        elif int(last_timestamp.replace(tzinfo=datetime.timezone.utc).timestamp()) == int(
                timestamp_now):  # if it's the same timestamp, we have to increment
            source = pkt["ip.src"]

            if source == current_host_name:
                upload_bytes_counter += int(pkt["length"])

                # contar os portos de origem
                if pkt["tcp.srcport"] in upload_ports:
                    upload_ports[pkt["tcp.srcport"]] += 1
                else:
                    upload_ports[pkt["tcp.srcport"]] = 1

            else:
                download_bytes_counter += int(pkt["length"])

                # contar os portos de origem
                if pkt["tcp.srcport"] in download_ports:
                    download_ports[pkt["tcp.srcport"]] += 1
                else:
                    download_ports[pkt["tcp.srcport"]] = 1

        last_timestamp = datetime.datetime.strptime(pkt["sniff_time"], "%Y-%m-%d %H:%M:%S.%f")

    # ack and inc index

    index += 1

    """
    when the size_bytes get's some value it will discard  old bytes and only X most recent bytes will be take in account
    """

    oWnd = int(unknown_data_bytes_counter.shape[0] / 3)

    if oWnd >= 20:
        break_data = breakData(unknown_data_bytes_counter, oWnd=oWnd)

        features_data = extractFeatures(break_data)[0]
        features_dataS = extractFeaturesSilence(break_data)[0]
        features_dataW = extractFeaturesWavelet(break_data)[0]
        unknown_data_features = np.hstack((features_data, features_dataS, features_dataW))

        # based on distances
        result = classify_distances(unknown_data_features, result="YouTube")

        sys.stdout.write("\r{}".format(result[0][0]))
        sys.stdout.flush()
    else:
        sys.stdout.write("\rWait a moment, we are recording data...")
        sys.stdout.flush()

    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == '__main__':
    queue_name = "packets"

    rabbitMQ.setup_queue(queue_name)

    rabbitMQ.channel.basic_consume(callback,
                                   queue=queue_name,
                                   no_ack=False)

    rabbitMQ.channel.start_consuming()
