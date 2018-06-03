from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pickle
import os
from colorama import Fore, Back, Style
import operator


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/")

from classifier.utils.classify import generate_name


def classify_neuronalNetworks(unknown_data_features, result="Mining", printing=False):
    with open(DATA_PATH + "bin/features_data.bin", 'rb') as f:
        allFeatures, Classes, oClass = pickle.load(f)

    centroids = {}
    for c in range(len(Classes)):
        pClass = (oClass == c).flatten()
        centroids.update({c: np.mean(allFeatures[pClass, :], axis=0)})

    allFeatures = allFeatures[:, :unknown_data_features.shape[1]]

    scaler = StandardScaler()
    NormAllFeatures = scaler.fit_transform(allFeatures)

    NormAllTestFeatures = scaler.fit_transform(unknown_data_features)

    pca = PCA(n_components=len(Classes), svd_solver='full')
    NormPcaFeatures = pca.fit(NormAllFeatures).transform(NormAllFeatures)

    NormTestPcaFeatures = pca.fit(NormAllTestFeatures).transform(NormAllTestFeatures)

    result_dict = {}

    for classes in Classes.values():
        result_dict[generate_name(classes)] = 0

    alpha = 1
    max_iter = 100000
    clf = MLPClassifier(solver='lbfgs', alpha=alpha, hidden_layer_sizes=(100,), max_iter=max_iter)
    clf.fit(NormPcaFeatures, oClass)
    LT = clf.predict(NormTestPcaFeatures)

    nObsTest, nFea = NormTestPcaFeatures.shape

    for i in range(nObsTest):
        result_dict[generate_name(Classes[LT[i]])] += 1

    if printing:
        print("\n" + Back.BLUE + Fore.WHITE + "# -> Final Results\n" + Style.RESET_ALL)

        print(Fore.BLUE + "Classification based on Neural Networks:" + Style.RESET_ALL)

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
