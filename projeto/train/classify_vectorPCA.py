from sklearn import svm
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from train.classify import extractFeatures, extractFeaturesSilence, extractFeaturesWavelet



def classify_vectorPCA(allFeatures, Classes, oClass, yt_test, browsing_test, mining_test, scales):
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

    print('\n-- Classification based on Support Vector Machines  (PCA Features) --')
    svc = svm.SVC(kernel='linear').fit(NormPcaFeatures, oClass)
    rbf_svc = svm.SVC(kernel='rbf').fit(NormPcaFeatures, oClass)
    poly_svc = svm.SVC(kernel='poly', degree=2).fit(NormPcaFeatures, oClass)
    lin_svc = svm.LinearSVC().fit(NormPcaFeatures, oClass)

    L1 = svc.predict(NormTestPcaFeatures)
    print('class (from test PCA features with SVC):', L1)
    L2 = rbf_svc.predict(NormTestPcaFeatures)
    print('class (from test PCA features with Kernel RBF):', L2)
    L3 = poly_svc.predict(NormTestPcaFeatures)
    print('class (from test PCA features with Kernel poly):', L3)
    L4 = lin_svc.predict(NormTestPcaFeatures)
    print('class (from test PCA features with Linear SVC):', L4)
    print('\n')

    nObsTest, nFea = NormTestPcaFeatures.shape
    for i in range(nObsTest):
        print('Obs: {:2}: SVC->{} | Kernel RBF->{} | Kernel Poly->{} | LinearSVC->{}'.format(i, Classes[L1[i]],
                                                                                             Classes[L2[i]],
                                                                                             Classes[L3[i]],
                                                                                             Classes[L4[i]]))