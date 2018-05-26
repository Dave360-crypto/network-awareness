from sklearn.cluster import KMeans
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pickle
import os
from colorama import Fore, Back, Style
import operator


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/")

def classify_clustering(unknown_data_features, result="Mining"):
    with open(DATA_PATH + "bin/features_data.bin", 'rb') as f:
        allFeatures, Classes, oClass = pickle.load(f)

    allFeatures = allFeatures[:, :unknown_data_features.shape[1]]

    pca = PCA(n_components=3, svd_solver='full')
    pcaFeatures = pca.fit(allFeatures).transform(allFeatures)

    centroids = {}
    for c in range(3):
        pClass = (oClass == c).flatten()
        centroids.update({c: np.mean(allFeatures[pClass, :], axis=0)})

    scaler = StandardScaler()
    NormAllFeatures = scaler.fit_transform(allFeatures)

    NormAllTestFeatures = scaler.fit_transform(unknown_data_features)

    pca = PCA(n_components=3, svd_solver='full')
    NormPcaFeatures = pca.fit(NormAllFeatures).transform(NormAllFeatures)

    NormTestPcaFeatures = pca.fit(NormAllTestFeatures).transform(NormAllTestFeatures)

    #print('\n-- Classification based on Clustering (Kmeans) --')
    # K-means assuming 3 clusters
    centroids = np.array([])
    for c in range(3):
        pClass = (oClass == c).flatten()
        centroids = np.append(centroids, np.mean(NormPcaFeatures[pClass, :], axis=0))
    centroids = centroids.reshape((3, 3))

    result_dict = {}

    for classes in Classes.values():
        result_dict[classes] = 0

    kmeans = KMeans(init=centroids, n_clusters=3)
    kmeans.fit(NormPcaFeatures)
    labels = kmeans.labels_
    #print('Labels:', labels)

    # Determines and quantifies the presence of each original class observation in each cluster
    KMclass = np.zeros((3, 3))
    for cluster in range(3):
        p = (labels == cluster)
        aux = oClass[p]
        for c in range(3):
            KMclass[cluster, c] = np.sum(aux == c)

    probKMclass = KMclass / np.sum(KMclass, axis=1)[:, np.newaxis]
    nObsTest, nFea = NormTestPcaFeatures.shape
    for i in range(nObsTest):
        x = NormTestPcaFeatures[i, :].reshape((1, nFea))
        label = kmeans.predict(x)
        testClass = 100 * probKMclass[label, :].flatten()
        
        testClass = np.argsort(testClass)[-1]

        result_dict[Classes[testClass]] += 1


    print("\n" + Back.BLUE + Fore.WHITE + "# -> Final Results\n" + Style.RESET_ALL)

    print(Fore.BLUE + "Classification based on Clustering (Kmeans):" + Style.RESET_ALL)

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