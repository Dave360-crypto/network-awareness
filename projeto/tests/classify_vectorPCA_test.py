import numpy as np

import sys
import os

sys.path.append("..")

from classifier.classify import breakData, extractFeatures, extractFeaturesWavelet, extractFeaturesSilence
from classifier.vectorPCA.classify_vectorPCA import classify_vectorPCA


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
    classify_vectorPCA(unknown_data_features)