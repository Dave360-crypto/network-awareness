import numpy as np
import os, sys
import pickle

from classifier.utils.classify import breakTrainTest, extractFeatures, extractFeaturesWavelet, extractFeaturesSilence


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/")

WINDOW = 120
SCALES = [2, 4, 8, 16, 32, 64, 128, 256]


def make_observation_features(class_idx, file_name):
    with open(DATA_PATH + file_name, 'rb') as f:
        comm_up_down, upload_ports, download_ports = pickle.load(f)

    comm_train, comm_test = breakTrainTest(comm_up_down, oWnd=WINDOW)

    features_comm, oClass_comm = extractFeatures(comm_train, Class=class_idx)
    features_commS, oClass_commS = extractFeaturesSilence(comm_train, Class=class_idx)
    features_commW, oClass_commW = extractFeaturesWavelet(comm_train, SCALES, Class=class_idx)

    return (features_comm, oClass_comm), (features_commS, oClass_commS), (features_commW, oClass_commW)


if __name__ == '__main__':
    observations = [
        "netflix_comm_record.bin",
        "spotify_comm_record.bin",
        "mining_cryptonight_comm_record.bin",
        "mining_x11_comm_record.bin",
        "mining_keccak_comm_record.bin"
    ]

    features = []
    featuresS = []
    featuresW = []

    oClass = []
    oClassS = []
    oClassW = []

    Classes = dict()

    for idx, observation in enumerate(observations):
        (features_comm, oClass_comm), (features_commS, oClass_commS), (features_commW, oClass_commW) = make_observation_features(idx, observation)

        # save features
        features.append(features_comm)
        featuresS.append(features_commS)
        featuresW.append(features_commW)

        # save class
        oClass.append(oClass_comm)
        oClassS.append(oClass_commS)
        oClassW.append(oClass_commW)

        Classes[idx] = observation.replace("_comm_record.bin", "").replace("_", " ").capitalize()

    features = np.vstack(tuple(features))
    oClass = np.vstack(tuple(oClass))

    featuresS = np.vstack(tuple(featuresS))
    oClassS = np.vstack(tuple(oClassS))

    featuresW = np.vstack(tuple(featuresW))
    oClassW = np.vstack(tuple(oClassW))

    allFeatures = np.hstack((features, featuresS, featuresW))

    with open(DATA_PATH + "bin/features_data.bin", 'wb') as f:
        pickle.dump((allFeatures, Classes, oClass), f)
