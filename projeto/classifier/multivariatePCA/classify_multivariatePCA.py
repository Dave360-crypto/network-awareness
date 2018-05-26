from scipy.stats import multivariate_normal
import numpy as np
from sklearn.decomposition import PCA
import pickle
import os
from colorama import Fore, Back, Style
import operator


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/")

def classify_multivaritePCA(unknown_data_features, result="Mining"):
    with open(DATA_PATH + "bin/features_data.bin", 'rb') as f:
        allFeatures, Classes, oClass = pickle.load(f)

    allFeatures = allFeatures[:, :unknown_data_features.shape[1]]

    pca = PCA(n_components=3, svd_solver='full')
    pcaFeatures = pca.fit(allFeatures).transform(allFeatures)

    centroids = {}
    for c in range(3):
        pClass = (oClass == c).flatten()
        centroids.update({c: np.mean(allFeatures[pClass, :], axis=0)})

    # print('Test Features Size:', unknown_data_features.shape)

    # print('\n-- Classification based on Multivariate PDF (PCA Features) --')
    means = {}
    for c in range(3):
        pClass = (oClass == c).flatten()
        means.update({c: np.mean(pcaFeatures[pClass, :], axis=0)})
    # print(means)

    covs = {}
    for c in range(3):
        pClass = (oClass == c).flatten()
        covs.update({c: np.cov(pcaFeatures[pClass, :], rowvar=0)})
    #print(covs)

    testpcaFeatures = pca.transform(unknown_data_features)  # uses pca fitted above, only transforms test data
    # print(testpcaFeatures)
    nObsTest, nFea = testpcaFeatures.shape

    result_dict = {}

    for classes in Classes.values():
        result_dict[classes] = 0

    for i in range(nObsTest):
        x = testpcaFeatures[i, :]
        probs = np.array([multivariate_normal.pdf(x, means[0]), multivariate_normal.pdf(x, means[1]),
                          multivariate_normal.pdf(x, means[2])])

        #probs = np.array([multivariate_normal.pdf(x, means[0], covs[0]), multivariate_normal.pdf(x, means[1], covs[1]),
        #                  multivariate_normal.pdf(x, means[2], covs[2])])

        testClass = np.argsort(probs)[-1]

        result_dict[Classes[testClass]] += 1

    print("\n" + Back.BLUE + Fore.WHITE + "# -> Final Results\n" + Style.RESET_ALL)

    print(Fore.BLUE + "MultivariatePCA:" + Style.RESET_ALL)

    first = True

    for key, value in sorted(result_dict.items(), key=operator.itemgetter(1), reverse=True):
        if first and key == result:
            print(Fore.GREEN + key + ": " + str(int(value / nObsTest * 100)) + "%" + Style.RESET_ALL)
        elif first:
            print(Fore.RED + key + ": " + str(int(value / nObsTest * 100)) + "%" + Style.RESET_ALL)
        else:
            print(key + ": " + str(int(value / nObsTest * 100)) + "%")

        first = False

    return {
        "result": result
    }
