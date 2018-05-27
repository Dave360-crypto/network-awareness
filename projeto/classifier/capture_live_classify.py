import numpy as np
import os, pickle

from classifier.classify import breakData, extractFeatures, extractFeaturesSilence, extractFeaturesWavelet
from classifier.clustering.classify_clustering import classify_clustering
from classifier.distances.classify_distances import classify_distances
from classifier.multivariatePCA.classify_multivariatePCA import classify_multivaritePCA
from classifier.neuronalNetworks.classify_neuronalNetworks import classify_neuronalNetworks
from classifier.vector.classify_vector import classify_vector
from classifier.vectorPCA.classify_vectorPCA import classify_vectorPCA


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "classifier/data/")

with open(DATA_PATH + "bin/live_data_processed.bin", 'rb') as f:
    unknown_data = pickle.load(f)

oWnd = 100
nSamples = oWnd * 3

unknown_data = unknown_data[:nSamples, :]

f.close()

break_data = breakData(unknown_data, oWnd=oWnd)

features_data = extractFeatures(break_data)[0]
features_dataS = extractFeaturesSilence(break_data)[0]
features_dataW = extractFeaturesWavelet(break_data)[0]
unknown_data_features = np.hstack((features_data, features_dataS, features_dataW))

# based on vector
classify_vector(unknown_data_features, result="YouTube")

# based on vector PCA
classify_vectorPCA(unknown_data_features, result="YouTube")

# based on multivariate PCA
classify_multivaritePCA(unknown_data_features, result="YouTube")

# based on distances
classify_distances(unknown_data_features, result="YouTube")

# based on clustering (Kmeans)
classify_clustering(unknown_data_features, result="YouTube")

# based on neural networks
classify_neuronalNetworks(unknown_data_features, result="YouTube")
