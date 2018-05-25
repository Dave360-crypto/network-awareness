import numpy as np
from classifier.classify import extractFeatures, extractFeaturesWavelet, extractFeaturesSilence, breakData
from classifier.vector.classify_vector import classify_vector

import sys, os
sys.path.append("..")

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
    data = breakData(unknown_data)

    # extract features of the unknown break data

    features_data, oClass_data = extractFeatures(data)

    features = np.vstack((features_data))
    oClass = np.vstack((oClass_data))

    features_dataS, oClass_data = extractFeaturesSilence(data)

    featuresS = np.vstack((features_dataS))
    oClass = np.vstack((oClass_data))

    scales = [2, 4, 8, 16, 32, 64, 128, 256]
    features_dataW, oClass_data = extractFeaturesWavelet(data, scales)

    featuresW = np.vstack((features_dataW))
    oClass = np.vstack((oClass_data))

    """
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
    

    features_ytW, oClass_yt = extractFeaturesWavelet(yt_train, scales, Class=0)
    features_browsingW, oClass_browsing = extractFeaturesWavelet(browsing_train, scales, Class=1)
    features_miningW, oClass_mining = extractFeaturesWavelet(mining_train, scales, Class=2)
    
    featuresW = np.vstack((features_ytW, features_browsingW, features_miningW))
    oClass = np.vstack((oClass_yt, oClass_browsing, oClass_mining))
    """
    print(oClass)

    allFeatures = np.hstack((features, featuresS, featuresW))

    classify_vector(allFeatures, Classes, oClass, scales, data)