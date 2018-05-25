import numpy as np

import sys, os
sys.path.append("..")

from classifier.classify import breakTrainTest, extractFeatures, extractFeaturesWavelet, extractFeaturesSilence, breakData
from classifier.vector.classify_vector import classify_vector


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "classifier/data/")


if __name__ == '__main__':
    # classes
    Classes = {0: 'YouTube', 1: 'Browsing', 2: 'Mining'}

    # loading the initial files...
    yt = np.loadtxt(DATA_PATH + 'initialDataFiles/YouTube.dat')
    browsing = np.loadtxt(DATA_PATH + 'initialDataFiles/Browsing.dat')
    mining = np.loadtxt(DATA_PATH + 'mining_download_upload_bytes.dat')

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
    yt_train, yt_test = breakTrainTest(yt)
    browsing_train, browsing_test = breakTrainTest(browsing)
    mining_train, mining_test = breakTrainTest(mining)

    features_yt, oClass_yt = extractFeatures(yt_train, Class=0)
    features_browsing, oClass_browsing = extractFeatures(browsing_train, Class=1)
    features_mining, oClass_mining = extractFeatures(mining_train, Class=2)

    features = np.vstack((features_yt, features_browsing, features_mining))
    oClass = np.vstack((oClass_yt, oClass_browsing, oClass_mining))

    features_ytS, oClass_yt = extractFeaturesSilence(yt_train, Class=0)
    features_browsingS, oClass_browsing = extractFeaturesSilence(browsing_train, Class=1)
    features_miningS, oClass_mining = extractFeaturesSilence(mining_train, Class=2)

    featuresS = np.vstack((features_ytS, features_browsingS, features_miningS))
    oClass = np.vstack((oClass_yt, oClass_browsing, oClass_mining))

    scales = [2, 4, 8, 16, 32, 64, 128, 256]
    features_ytW, oClass_yt = extractFeaturesWavelet(yt_train, scales, Class=0)
    features_browsingW, oClass_browsing = extractFeaturesWavelet(browsing_train, scales, Class=1)
    features_miningW, oClass_mining = extractFeaturesWavelet(mining_train, scales, Class=2)

    featuresW = np.vstack((features_ytW, features_browsingW, features_miningW))
    oClass = np.vstack((oClass_yt, oClass_browsing, oClass_mining))

    allFeatures = np.hstack((features, featuresS, featuresW))

    classify_vector(unknown_data_features, Classes, oClass, scales, break_data)