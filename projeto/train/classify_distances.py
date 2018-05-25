import numpy as np

from train.classify import distance, extractFeatures, extractFeaturesSilence, extractFeaturesWavelet


def classify_distances(allFeatures, Classes, oClass, yt_test, browsing_test, mining_test, scales):
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

    print('\n-- Classification based on Distances --')
    nObsTest, nFea = alltestFeatures.shape
    for i in range(nObsTest):
        x = alltestFeatures[i]
        dists = [distance(x, centroids[0]), distance(x, centroids[1]), distance(x, centroids[2])]
        ndists = dists / np.sum(dists)
        testClass = np.argsort(dists)[0]
        print(
            'Obs: {:2}: Normalized Distances to Centroids: [{:.4f},{:.4f},{:.4f}] -> Classification: {} -> {}'.format(i,
                                                                                                                      *ndists,testClass, Classes[testClass]))
