import numpy as np

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


if __name__ == '__main__':
    # classify unknown data
    unknown_data = np.loadtxt(DATA_PATH + 'mining_download_upload_bytes.dat')

    # break data
    break_data = breakData(unknown_data)

    # extract features of the unknown break data
    features_data = extractFeatures(break_data)[0]
    features_dataS = extractFeaturesSilence(break_data)[0]
    features_dataW = extractFeaturesWavelet(break_data)[0]
    unknown_data_features = np.hstack((features_data, features_dataS, features_dataW))

    # creating train and test data for each Class (YouTube, Browsing and Mining)
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

