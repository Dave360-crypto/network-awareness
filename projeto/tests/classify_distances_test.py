import numpy as np

from os import listdir
from os.path import isfile, join
import sys
import os
import pickle

sys.path.append("..")

from classifier.utils.classify import breakData, extractFeatures, extractFeaturesWavelet, extractFeaturesSilence, \
    generate_name_from_file
from classifier.distances.classify_distances import classify_distances


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "classifier/data/")

if __name__ == '__main__':
    observations = [f for f in listdir(DATA_PATH) if isfile(join(DATA_PATH, f)) and not f.startswith(".")]

    for file_name in observations:
        print("\n")
        print("filename: ", file_name, " Expected result:", generate_name_from_file(file_name))
        # classify unknown data
        # file_name = "mining_cryptonight_comm_record.bin"

        # classify unknown data
        try:
            with open(DATA_PATH + file_name, 'rb') as f:
                comm_up_down, a, b = pickle.load(f)
        except Exception:
            with open(DATA_PATH + file_name, 'rb') as f:
                comm_up_down = pickle.load(f)


        # break data
        break_data = breakData(comm_up_down)

        # extract features of the unknown break data
        features_data = extractFeatures(break_data)[0]
        features_dataS = extractFeaturesSilence(break_data)[0]
        features_dataW = extractFeaturesWavelet(break_data)[0]
        unknown_data_features = np.hstack((features_data, features_dataS, features_dataW))

        # creating train and test data for each Class (YouTube, Browsing and Mining)
        result = classify_distances(features_data, features_dataS, features_dataW, printing=True, result=generate_name_from_file(file_name))
