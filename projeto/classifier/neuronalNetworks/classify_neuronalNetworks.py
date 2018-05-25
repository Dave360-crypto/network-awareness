from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from classifier.classify import extractFeatures, extractFeaturesSilence, extractFeaturesWavelet


def classify_neuronalNetworks(allFeatures, Classes, oClass, yt_test, browsing_test, mining_test, scales):
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

    print('\n-- Classification based on Neural Networks --')

    alpha = 1
    max_iter = 100000
    clf = MLPClassifier(solver='lbfgs', alpha=alpha, hidden_layer_sizes=(100,), max_iter=max_iter)
    clf.fit(NormPcaFeatures, oClass)
    LT = clf.predict(NormTestPcaFeatures)
    print('class (from test PCA):', LT)

    nObsTest, nFea = NormTestPcaFeatures.shape
    for i in range(nObsTest):
        print('Obs: {:2}: Classification->{}'.format(i, Classes[LT[i]]))

