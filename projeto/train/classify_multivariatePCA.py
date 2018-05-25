from scipy.stats import multivariate_normal
import numpy as np
from sklearn.decomposition import PCA
from train.classify import extractFeatures, extractFeaturesSilence, extractFeaturesWavelet


def classify_multivaritePCA(allFeatures, Classes, oClass, yt_test, browsing_test, mining_test, scales):
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

    print('Test Features Size:', alltestFeatures.shape)

    print('\n-- Classification based on Multivariate PDF (PCA Features) --')
    means = {}
    for c in range(3):
        pClass = (oClass == c).flatten()
        means.update({c: np.mean(pcaFeatures[pClass, :], axis=0)})
    # print(means)

    covs = {}
    for c in range(3):
        pClass = (oClass == c).flatten()
        covs.update({c: np.cov(pcaFeatures[pClass, :], rowvar=0)})
    # print(covs)

    testpcaFeatures = pca.transform(alltestFeatures)  # uses pca fitted above, only transforms test data
    print(testpcaFeatures)
    nObsTest, nFea = testpcaFeatures.shape
    for i in range(nObsTest):
        x = testpcaFeatures[i, :]
        probs = np.array([multivariate_normal.pdf(x, means[0], covs[0]), multivariate_normal.pdf(x, means[1], covs[1]),
                          multivariate_normal.pdf(x, means[2], covs[2])])
        testClass = np.argsort(probs)[-1]

        print(
            'Obs: {:2}: Probabilities: [{:.4e},{:.4e},{:.4e}] -> Classification: {} -> {}'.format(i, *probs, testClass,
                                                                                                  Classes[testClass]))