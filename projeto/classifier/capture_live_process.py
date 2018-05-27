import numpy as np
import socket
import datetime
import os, pickle

from classifier.classify import breakData, extractFeatures, extractFeaturesSilence, extractFeaturesWavelet
from classifier.clustering.classify_clustering import classify_clustering
from classifier.distances.classify_distances import classify_distances
from classifier.multivariatePCA.classify_multivariatePCA import classify_multivaritePCA
from classifier.neuronalNetworks.classify_neuronalNetworks import classify_neuronalNetworks
from classifier.vector.classify_vector import classify_vector
from classifier.vectorPCA.classify_vectorPCA import classify_vectorPCA

upload_counter = 0
upload_bytes_counter = 0
download_bytes_counter = 0
upload_ports = {}
download_counter = 0
download_ports = {}
download_ports_counter = 0
upload_ports_counter = 0
upload_bytes = []
download_bytes = []

index = 0
count = 0
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "classifier/data/")

with open(DATA_PATH + "bin/live_data.bin", 'rb') as f:
    packets = pickle.load(f)

f.close()

last_timestamp = 0

for index, pkt in packets.items():
    source = pkt["ip.src"]
    if index == 0:
        if source == socket.gethostbyname(socket.gethostname()):
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

        last_timestamp = packets[index]["sniff_time"]
        continue

    timestamp_now = packets[index]["sniff_time"]
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

        if source == socket.gethostbyname(socket.gethostname()):
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

    last_timestamp = packets[index]["sniff_time"]

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

break_data = breakData(unknown_data)

features_data = extractFeatures(break_data)[0]
features_dataS = extractFeaturesSilence(break_data)[0]
features_dataW = extractFeaturesWavelet(break_data)[0]
unknown_data_features = np.hstack((features_data, features_dataS, features_dataW))

# based on vector
classify_vector(unknown_data_features)

# based on vector PCA
classify_vectorPCA(unknown_data_features)

# based on multivariate PCA
classify_multivaritePCA(unknown_data_features)

# based on distances
classify_distances(unknown_data_features)

#based on clustering (Kmeans)
classify_clustering(unknown_data_features)

# based on neural networks
classify_neuronalNetworks(unknown_data_features)