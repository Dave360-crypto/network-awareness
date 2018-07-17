import pyshark
import socket
import sys
import datetime
import numpy as np
from classifier.distances.classify_distances import classify_distances
from classifier.utils.classify import breakData, extractFeatures, extractFeaturesSilence, extractFeaturesWavelet
import traceback
# websocket
import tornado.ioloop
import tornado.web
import tornado.websocket
from threading import Thread
import logging
import json
import asyncio
import pickle
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "classifier/data/")

# logging
logging.basicConfig(level=logging.INFO)


# web socket clients connected.
clients = []

# bytes_counter by tcp service
tcp_services = dict()

# [END] ports counter (upload and download)

current_host_name = socket.gethostbyname(socket.gethostname())

# WINDOW

WINDOW = 120

last_timestamp_classify = datetime.datetime.now()


def thread_pyshark():
    # starting event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # pyshark filters
    capture = pyshark.LiveCapture(interface='en0', bpf_filter='tcp')
    # Bytes counter (download and upload)

    def classify(pkt):
        global tcp_services, current_host_name, last_timestamp_classify

        # verify if the tcp service has been already registered
        src_port = pkt["tcp.srcport"]
        dst_port = pkt["tcp.dstport"]
        
        # save the port to further update the tcp services dict
        port = dst_port
        
        if src_port in tcp_services.keys():
            # the packet belongs to one tcp service session
            service = tcp_services[src_port]
            port = src_port
        elif dst_port in tcp_services.keys():
            service = tcp_services[dst_port]
            port = dst_port
        else:
            # new tcp session, let's create it
            service = {
                "upload_bytes_counter": 0,
                "download_bytes_counter": 0,
                "last_timestamp": 0,
                "index": 0,
                "data_bytes_counter": np.array([[0, 0]])
            }

        # end verify

        source = pkt["ip.src"]

        if service["index"] == 0:
            if source == current_host_name:
                service["upload_bytes_counter"] += int(pkt["length"])
            else:
                service["download_bytes_counter"] += int(pkt["length"])

            service["last_timestamp"] = pkt["sniff_time"]
        else:
            # index != 0
            timestamp_now = pkt["sniff_time"]
            timestamp_now = timestamp_now.replace(tzinfo=datetime.timezone.utc).timestamp()

            delta_time = ((datetime.datetime.utcfromtimestamp(int(timestamp_now))) - service["last_timestamp"]).total_seconds()

            if delta_time >= 1:  # if passed more than one second, means we have to write n 0
                service["data_bytes_counter"] = np.append(service["data_bytes_counter"],
                                                          [[service["download_bytes_counter"],
                                                            service["upload_bytes_counter"]]], 0)

                for i in range(0, int(delta_time) - 1):
                    service["data_bytes_counter"] = np.append(service["data_bytes_counter"], [[0, 0]], 0)

                service["upload_bytes_counter"] = 0
                service["download_bytes_counter"] = 0

            elif int(service["last_timestamp"].replace(tzinfo=datetime.timezone.utc).timestamp()) == int(
                    timestamp_now):  # if it's the same timestamp, we have to increment
                source = pkt["ip.src"]

                if source == current_host_name:
                    service["upload_bytes_counter"] += int(pkt["length"])

                else:
                    service["download_bytes_counter"] += int(pkt["length"])

            service["last_timestamp"] = pkt["sniff_time"]

        # ack and inc index

        service["index"] += 1

        # update tcp services
        tcp_services[port] = service

        """
        Update the empty seconds for each tcp service that didn't receive any byte
        """
        for port in tcp_services.keys():
            service = tcp_services[port]

            timestamp_now = pkt["sniff_time"]
            timestamp_now = timestamp_now.replace(tzinfo=datetime.timezone.utc).timestamp()

            delta_time = ((datetime.datetime.utcfromtimestamp(int(timestamp_now))) - service["last_timestamp"]).total_seconds()

            if delta_time >= 3:  # if passed more than one second, means we have to write n 0
                service["data_bytes_counter"] = np.append(service["data_bytes_counter"],
                                                          [[service["download_bytes_counter"],
                                                            service["upload_bytes_counter"]]], 0)

                for i in range(0, int(delta_time) - 1):
                    service["data_bytes_counter"] = np.append(service["data_bytes_counter"], [[0, 0]], 0)

                service["upload_bytes_counter"] = 0
                service["download_bytes_counter"] = 0
                service["last_timestamp"] = pkt["sniff_time"]

            tcp_services[port] = service
        """
        When the size_bytes get's some value it will discard  old bytes and only X most recent bytes will be take in account
        """
        delta_time = (datetime.datetime.now() - last_timestamp_classify).total_seconds()

        if delta_time >= 1:
            # if passed more than one second, means we have to write n 0
            message = {}

            for port, service in tcp_services.items():
                if service["data_bytes_counter"].shape[0] >= WINDOW:

                    try:
                        # 121-120: 1: =>120, 2
                        data_bytes_counter = service["data_bytes_counter"][service["data_bytes_counter"].shape[0]-WINDOW:, :]

                        break_data = breakData(data_bytes_counter, oWnd=WINDOW)

                        features_data = extractFeatures(break_data)[0]
                        features_dataS = extractFeaturesSilence(break_data)[0]
                        features_dataW = extractFeaturesWavelet(break_data)[0]

                        # based on distances
                        result = dict(classify_distances(features_data, features_dataS, features_dataW, result="YouTube"))

                        # message
                        sum_results = result["Other"] + result["Mining"]

                        if sum_results > 0:
                            result["Other"] = (result["Other"] / sum_results) * 100
                            result["Mining"] = (result["Mining"] / sum_results) * 100

                            # association with service port
                            message[port] = result
                    except Exception as e:
                        message[port] = "Window size with only zeros ({})".format(service["data_bytes_counter"].shape[0])
                        """
                        print("Error, Port: {} Shape {}".format(port, str(service["data_bytes_counter"].shape)))

                        # print traceback
                        exc_type, exc_value, exc_traceback = sys.exc_info()

                        print("*** print_tb:")
                        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

                        print("*** print_exception:")
                        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
                        """
                else:
                    message[port] = "Not enough data ({})".format(service["data_bytes_counter"].shape[0])

            print("\r{}".format(str(json.dumps(message, sort_keys=True, indent=4))))

            send_message = dict()
            send_message["ports"] = message
            send_message["host"] = current_host_name

            for itm in clients:
                itm.write_message(json.dumps(send_message))

            # change last timestamp
            last_timestamp_classify = datetime.datetime.now()

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
    try:
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
    except KeyboardInterrupt:
        print("If you want you can record this session for input.")

        ports = input("Which ports do you want to select (answer with CSV)?\n {}: ".format(list(tcp_services.keys())))

        if ports == "all":
            ports = list(tcp_services.keys())
        else:
            ports = ports.replace(" ", "").split(",")

        for port in ports:
            prefix = input("\nPrefix name for the capture (port: {})?".format(port))

            with open(DATA_PATH + prefix + "_" + port + "_comm_record.bin", 'wb') as f:
                pickle.dump((tcp_services[port]["data_bytes_counter"]), f)
