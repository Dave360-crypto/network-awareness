import pyshark
import socket
import sys
import datetime
import numpy as np
from classifier.distances.classify_distances import classify_distances
from classifier.utils.classify import breakData, extractFeatures, extractFeaturesSilence, extractFeaturesWavelet

# websocket
import tornado.ioloop
import tornado.web
import tornado.websocket
from threading import Thread
import logging
import json
import asyncio

# logging
logging.basicConfig(level=logging.INFO)


# web socket clients connected.
clients = []

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

# WINDOW

WINDOW = 120


def thread_pyshark():
    # starting event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # pyshark filters
    capture = pyshark.LiveCapture(interface='en0', bpf_filter='tcp')
    # Bytes counter (download and upload)

    def classify(pkt):
        global index, last_timestamp, upload_bytes_counter, download_bytes_counter, unknown_data_bytes_counter, \
            upload_ports, download_ports, current_host_name

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

            last_timestamp = pkt["sniff_time"]
        else:
            # index != 0
            timestamp_now = pkt["sniff_time"]
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

            last_timestamp = pkt["sniff_time"]

        # ack and inc index

        index += 1

        """
        When the size_bytes get's some value it will discard  old bytes and only X most recent bytes will be take in account
        """
        if unknown_data_bytes_counter.shape[0] >= WINDOW:
            # websocket message
            message = [0, 0]

            # 121-120: 1: =>120, 2
            unknown_data_bytes_counter = unknown_data_bytes_counter[unknown_data_bytes_counter.shape[0]-WINDOW:, :]

            break_data = breakData(unknown_data_bytes_counter, oWnd=WINDOW)

            features_data = extractFeatures(break_data)[0]
            features_dataS = extractFeaturesSilence(break_data)[0]
            features_dataW = extractFeaturesWavelet(break_data)[0]
            unknown_data_features = np.hstack((features_data, features_dataS, features_dataW))

            # based on distances
            result = classify_distances(unknown_data_features, result="YouTube")

            sys.stdout.write("\rType: {} | Data size: {}".format(result[0][0], unknown_data_bytes_counter.shape[0]))
            sys.stdout.flush()

            # message
            sum_results = result[0][1] + result[1][1]

            if sum_results > 0:
                message = [result[1][1]/sum_results, result[0][1]/sum_results]

            for itm in clients:
                itm.write_message(json.dumps(message))
        else:
            sys.stdout.write("\rWait a moment, we are recording data... | Data size: {}".format(unknown_data_bytes_counter.shape[0]))
            sys.stdout.flush()

    def print_callback(pkt):
        classify({
            "ip.src": pkt.ip.src,
            "tcp.dstport": pkt.tcp.dstport,
            "length": pkt.length,
            "tcp.srcport": pkt.tcp.srcport,
            "sniff_time": pkt.sniff_time
        })

    # capture the packets
    capture.apply_on_packets(print_callback)

    # capture stopped
    sys.stdout.write("\rEnded!")
    sys.stdout.flush()


class SocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        logging.info('WebSocket opened')
        clients.append(self)
        self.write_message(json.dumps([0, 0]))

    def on_close(self):
        logging.info('WebSocket closed')
        clients.remove(self)


application = tornado.web.Application([
    (r'/ws', SocketHandler)
])


def startTornado():
    asyncio.set_event_loop(asyncio.new_event_loop())
    application.listen(1234)
    tornado.ioloop.IOLoop.instance().start()


def stopTornado():
    tornado.ioloop.IOLoop.instance().stop()


if __name__ == '__main__':
    logging.info('Starting thread PyShark')

    threadPyShark = Thread(target=thread_pyshark)
    threadPyShark.start()

    logging.info('Starting thread Tornado')

    threadTornado = Thread(target=startTornado)
    threadTornado.start()

    try:
        input("Server ready. Press enter to stop\n")
    except SyntaxError:
        pass

    logging.info('Disconnecting from PyShark..')
    logging.info('Disconnected from PyShark..')

    stopTornado()

    logging.info('See you...')
    exit(1)


