from sklearn.cluster import KMeans
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from train.classify import extractFeatures, extractFeaturesSilence, extractFeaturesWavelet

def classify_clustering(allFeatures, Classes, oClass, yt_test, browsing_test, mining_test, scales):
    pca = PCA(n_components=3, svd_solver='full')
    pcaFeatures = pca.fit(allFeatures).transform(allFeatures)

    centroids = {}
    for c in range(3):
        pClass = (oClass == c).flatten()
        centroids.update({c: np.mean(allFeatures[pClass, :], axis=0)})
    print('All Features Centroids:\n', centroids)

    testFeatures_yt, oClass_yt = extractFeatures(yt_test, Class=0)
    testFeatures_browsing, oClass_browsing = extractFeatures(browsing_test, Class=1)
    testFeatures_mining, oClass_mining = extractFeatures(mining_test, Class=2)
    testFeatures = np.vstack((testFeatures_yt, testFeatures_browsing, testFeatures_mining))

    testFeatures_ytS, oClass_yt = extractFeaturesSilence(yt_test, Class=0)
    testFeatures_browsingS, oClass_browsing = extractFeaturesSilence(browsing_test, Class=1)
    testFeatures_miningS, oClass_mining = extractFeaturesSilence(mining_test, Class=2)
    testFeaturesS = np.vstack((testFeatures_ytS, testFeatures_browsingS, testFeatures_miningS))

    testFeatures_ytW, oClass_yt = extractFeaturesWavelet(yt_test, scales, Class=0)
    testFeatures_browsingW, oClass_browsing = extractFeaturesWavelet(browsing_test, scales, Class=1)
    testFeatures_miningW, oClass_mining = extractFeaturesWavelet(mining_test, scales, Class=2)
    testFeaturesW = np.vstack((testFeatures_ytW, testFeatures_browsingW, testFeatures_miningW))

    alltestFeatures = np.hstack((testFeatures, testFeaturesS, testFeaturesW))

    scaler = StandardScaler()
    NormAllFeatures = scaler.fit_transform(allFeatures)

    NormAllTestFeatures = scaler.fit_transform(alltestFeatures)

    pca = PCA(n_components=3, svd_solver='full')
    NormPcaFeatures = pca.fit(NormAllFeatures).transform(NormAllFeatures)

    NormTestPcaFeatures = pca.fit(NormAllTestFeatures).transform(NormAllTestFeatures)

    print('\n-- Classification based on Clustering (Kmeans) --')
    # K-means assuming 3 clusters
    centroids = np.array([])
    for c in range(3):
        pClass = (oClass == c).flatten()
        centroids = np.append(centroids, np.mean(NormPcaFeatures[pClass, :], axis=0))
    centroids = centroids.reshape((3, 3))
    print('PCA (pcaFeatures) Centroids:\n', centroids)

    kmeans = KMeans(init=centroids, n_clusters=3)
    kmeans.fit(NormPcaFeatures)
    labels = kmeans.labels_
    print('Labels:', labels)

    # Determines and quantifies the presence of each original class observation in each cluster
    KMclass = np.zeros((3, 3))
    for cluster in range(3):
        p = (labels == cluster)
        aux = oClass[p]
        for c in range(3):
            KMclass[cluster, c] = np.sum(aux == c)

    probKMclass = KMclass / np.sum(KMclass, axis=1)[:, np.newaxis]
    print(probKMclass)
    nObsTest, nFea = NormTestPcaFeatures.shape
    for i in range(nObsTest):
        x = NormTestPcaFeatures[i, :].reshape((1, nFea))
        label = kmeans.predict(x)
        testClass = 100 * probKMclass[label, :].flatten()
        print('Obs: {:2}: Probabilities beeing in each class: [{:.2f}%,{:.2f}%,{:.2f}%]'.format(i, *testClass))


    # DBSCAN assuming a neighborhood maximum distance of 1e11
    dbscan = DBSCAN(eps=10000)
    dbscan.fit(pcaFeatures)
    labels = dbscan.labels_
    print('Labels:', labels)