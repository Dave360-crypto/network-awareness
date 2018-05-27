import numpy as np
import pickle
import os
from colorama import Fore, Back, Style
import operator


from classifier.utils.classify import distance


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/")


def classify_distances(unknown_data_features, result="Mining", printing=False):
    with open(DATA_PATH + "bin/features_data.bin", 'rb') as f:
        allFeatures, Classes, oClass = pickle.load(f)

    allFeatures = allFeatures[:, :unknown_data_features.shape[1]]

    centroids = {}
    for c in range(3):
        pClass = (oClass == c).flatten()
        centroids.update({c: np.mean(allFeatures[pClass, :], axis=0)})

    result_dict = {}

    for classes in Classes.values():
        result_dict[classes] = 0

    nObsTest, nFea = unknown_data_features.shape

    for i in range(nObsTest):
        x = unknown_data_features[i]
        dists = [distance(x, centroids[0]), distance(x, centroids[1]), distance(x, centroids[2])]
        ndists = dists / np.sum(dists)
        testClass = np.argsort(dists)[0]

        result_dict[Classes[testClass]] += 1

    if printing:
        print("\n" + Back.BLUE + Fore.WHITE + "# -> Final Results\n" + Style.RESET_ALL)

        print(Fore.BLUE + "Classification based on Distances:" + Style.RESET_ALL)

        first = True

        for key, value in sorted(result_dict.items(), key=operator.itemgetter(1), reverse=True):
            if first and key == result:
                print(Fore.GREEN + key + ": " + str(int(value / nObsTest * 100)) + "%" + Style.RESET_ALL)
            elif first:
                print(Fore.RED + key + ": " + str(int(value / nObsTest * 100)) + "%" + Style.RESET_ALL)
            else:
                print(key + ": " + str(int(value / nObsTest * 100)) + "%")

            first = False

    return result
