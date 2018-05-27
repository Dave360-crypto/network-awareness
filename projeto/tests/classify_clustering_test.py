import numpy as np

import sys, os
sys.path.append("..")

from classifier.utils.classify import breakTrainTest, extractFeatures, extractFeaturesWavelet, extractFeaturesSilence, \
    breakData
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
    classify_clustering(unknown_data_features, printing=True)