from sklearn import svm
import numpy as np
from sklearn.preprocessing import StandardScaler
from classifier.classify import extractFeatures, extractFeaturesSilence, extractFeaturesWavelet


def classify_vector(allFeatures, Classes, oClass, scales, interval_data):

    testFeatures_data, oClass_data = extractFeatures(interval_data)
    testFeatures = np.vstack((testFeatures_data))

    testFeaturesv_data, oClass__data = extractFeaturesSilence(interval_data)
    testFeaturesS = np.vstack(testFeaturesv_data)

    testFeatures_data, oClass__data = extractFeaturesWavelet(interval_data, scales)
    testFeaturesW = np.vstack((testFeatures_data))

    """
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
    """

    alltestFeatures = np.hstack((testFeatures, testFeaturesS, testFeaturesW))

    scaler = StandardScaler()
    NormAllFeatures = scaler.fit_transform(allFeatures)

    NormAllTestFeatures = scaler.fit_transform(alltestFeatures)

    print('\n-- Classification based on Support Vector Machines --')
    svc = svm.SVC(kernel='linear').fit(NormAllFeatures, oClass)
    rbf_svc = svm.SVC(kernel='rbf').fit(NormAllFeatures, oClass)
    poly_svc = svm.SVC(kernel='poly', degree=2).fit(NormAllFeatures, oClass)
    lin_svc = svm.LinearSVC().fit(NormAllFeatures, oClass)

    L1 = svc.predict(NormAllTestFeatures)
    print('class (from test PCA features with SVC):', L1)
    L2 = rbf_svc.predict(NormAllTestFeatures)
    print('class (from test PCA features with Kernel RBF):', L2)
    L3 = poly_svc.predict(NormAllTestFeatures)
    print('class (from test PCA features with Kernel poly):', L3)
    L4 = lin_svc.predict(NormAllTestFeatures)
    print('class (from test PCA features with Linear SVC):', L4)
    print('\n')

    nObsTest, nFea = NormAllTestFeatures.shape
    for i in range(nObsTest):
        print('Obs: {:2}: SVC->{} | Kernel RBF->{} | Kernel Poly->{} | LinearSVC->{}'.format(i, Classes[L1[i]],
                                                                                             Classes[L2[i]],
                                                                                             Classes[L3[i]],
                                                                                             Classes[L4[i]]))
