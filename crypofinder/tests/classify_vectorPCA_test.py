import numpy as np
import pickle
import sys
import os

sys.path.append("..")

from classifier.utils.classify import breakData, extractFeatures, extractFeaturesWavelet, extractFeaturesSilence, \
    generate_name_from_file
from classifier.vectorPCA.classify_vectorPCA import classify_vectorPCA


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "classifier/data/")


if __name__ == '__main__':
    # classify unknown data
    file_name = "netflix_comm_record.bin"

    # classify unknown data
    with open(DATA_PATH + file_name, 'rb') as f:
        comm_up_down, upload_ports, download_ports = pickle.load(f)

    # break data
    break_data = breakData(comm_up_down)

    # extract features of the unknown break data
    features_data = extractFeatures(break_data)[0]
    features_dataS = extractFeaturesSilence(break_data)[0]
    features_dataW = extractFeaturesWavelet(break_data)[0]
    unknown_data_features = np.hstack((features_data, features_dataS, features_dataW))

    # creating train and test data for each Class (YouTube, Browsing and Mining)
    classify_vectorPCA(unknown_data_features, printing=True, result=generate_name_from_file(file_name))
