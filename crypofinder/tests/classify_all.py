import numpy as np
import pickle
import sys, os

from classifier.neuronalNetworks.classify_neuronalNetworks import classify_neuronalNetworks

sys.path.append("..")

from classifier.utils.classify import extractFeatures, extractFeaturesWavelet, extractFeaturesSilence, breakData
from classifier.vector.classify_vector import classify_vector
from classifier.vectorPCA.classify_vectorPCA import classify_vectorPCA
from classifier.multivariatePCA.classify_multivariatePCA import classify_multivaritePCA
from classifier.distances.classify_distances import classify_distances
from classifier.clustering.classify_clustering import classify_clustering


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "classifier/data/")

WINDOW = 120

if __name__ == '__main__':
    observations = [
        "netflix_comm_record.bin",
        "spotify_comm_record.bin",
        "mining_cryptonight_comm_record.bin",
        "mining_x11_comm_record.bin",
        "mining_keccak_comm_record.bin"
    ]

    for observation in observations:
        name = observation.replace("_comm_record.bin", "").replace("_", " ").capitalize().split(" ")[0]

        if name != "Mining":
            name = "Other"

        print("\n########################################## " + name + " ###################################")

        # classify unknown data
        with open(DATA_PATH + observation, 'rb') as f:
            comm_up_down, upload_ports, download_ports = pickle.load(f)

        # break data
        break_data = breakData(comm_up_down, oWnd=WINDOW)

        # extract features of the unknown break data
        features_data = extractFeatures(break_data)[0]
        features_dataS = extractFeaturesSilence(break_data)[0]
        features_dataW = extractFeaturesWavelet(break_data)[0]
        unknown_data_features = np.hstack((features_data, features_dataS, features_dataW))

        # creating train and test data for each Class (YouTube, Browsing and Mining)
        # based on vector
        classify_vector(unknown_data_features, printing=True, result=name)

        # based on vector PCA
        classify_vectorPCA(unknown_data_features, printing=True, result=name)

        # based on multivariate PCA
        classify_multivaritePCA(unknown_data_features, printing=True, result=name)

        # based on distances
        classify_distances(unknown_data_features, printing=True, result=name)

        #based on clustering (Kmeans)
        classify_clustering(unknown_data_features, printing=True, result=name)

        # based on neural networks
        classify_neuronalNetworks(unknown_data_features, printing=True, result=name)

