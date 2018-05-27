import numpy as np
import warnings
from classifier import scalogram

warnings.filterwarnings('ignore')


def breakTrainTest(data, oWnd=300, trainPerc=0.5):
    nSamp, nCols = data.shape
    nObs = int(nSamp / oWnd)
    data_obs = data[:nObs * oWnd].reshape((nObs, oWnd, nCols))

    data_withoutzeros = []

    for i in range(0, nObs):
        mean = np.mean(data_obs[i, :, :], axis=0)
        if mean[0] == 0 and mean[1] == 0:
            pass
        else:
            data_withoutzeros.append(data_obs[i, :, :])

    data_withoutzeros = np.array(data_withoutzeros)

    nObs, oWnd, nCols = data_withoutzeros.shape

    order = np.random.permutation(nObs)
    order = np.arange(nObs)  # Comment out to random split

    nTrain = int(nObs * trainPerc)

    data_withoutzeros = data_withoutzeros[:nObs * oWnd].reshape((nObs, oWnd, nCols))

    data_train = data_withoutzeros[order[:nTrain], :, :]
    data_test = data_withoutzeros[order[nTrain:], :, :]

    return (data_train, data_test)


def breakData(data, oWnd=300):
    """
    Used to break the data in observation windows. It will remove the windows with the mean (up and down) equal to zero.
    :param data: all data
    :param oWnd: window size
    :return: data without zeros reshaped in obs wnd and cols
    """
    nSamp, nCols = data.shape
    nObs = int(nSamp / oWnd)
    data_obs = data[:nObs * oWnd].reshape((nObs, oWnd, nCols))

    data_withoutzeros = []

    for i in range(0, nObs):
        mean = np.mean(data_obs[i, :, :], axis=0)
        if mean[0] == 0 and mean[1] == 0:
            pass
        else:
            data_withoutzeros.append(data_obs[i, :, :])

    data_withoutzeros = np.array(data_withoutzeros)

    nObs, oWnd, nCols = data_withoutzeros.shape

    data_withoutzeros = data_withoutzeros[:nObs * oWnd].reshape((nObs, oWnd, nCols))

    return data_withoutzeros


def extractFeatures(data, Class=0):
    features = []
    #print(data)
    nObs, nSamp, nCols = data.shape
    oClass = np.ones((nObs, 1)) * Class
    for i in range(nObs):
        M1 = np.mean(data[i, :, :], axis=0)
        # Md1=np.median(data[i,:,:],axis=0)
        Std1 = np.std(data[i, :, :], axis=0)
        # S1=stats.skew(data[i,:,:])
        # K1=stats.kurtosis(data[i,:,:])
        p = [75, 90, 95]
        Pr1 = np.array(np.percentile(data[i, :, :], p, axis=0)).T.flatten()

        # faux=np.hstack((M1,Md1,Std1,S1,K1,Pr1))
        faux = np.hstack((M1, Std1, Pr1))
        features.append(faux)

    return (np.array(features), oClass)


def extratctSilence(data, threshold=256):
    if (data[0] <= threshold):
        s = [1]
    else:
        s = []
    for i in range(1, len(data)):
        if (data[i - 1] > threshold and data[i] <= threshold):
            s.append(1)
        elif (data[i - 1] <= threshold and data[i] <= threshold):
            s[-1] += 1

    return (s)


def extractFeaturesSilence(data, Class=0):
    features = []
    nObs, nSamp, nCols = data.shape
    oClass = np.ones((nObs, 1)) * Class
    for i in range(nObs):
        silence_features = np.array([])
        for c in range(nCols):
            silence = extratctSilence(data[i, :, c], threshold=0)
            if len(silence) > 0:
                silence_features = np.append(silence_features, [np.mean(silence), np.var(silence)])
            else:
                silence_features = np.append(silence_features, [0, 0])

        features.append(silence_features)

    return (np.array(features), oClass)


def extractFeaturesWavelet(data, scales=[2, 4, 8, 16, 32], Class=0):
    features = []
    nObs, nSamp, nCols = data.shape
    oClass = np.ones((nObs, 1)) * Class
    for i in range(nObs):
        scalo_features = np.array([])
        for c in range(nCols):
            # fixed scales->fscales
            scalo, fscales = scalogram.scalogramCWT(data[i, :, c], scales)
            scalo_features = np.append(scalo_features, scalo)

        features.append(scalo_features)

    return (np.array(features), oClass)


def distance(c, p):
    return (np.sqrt(np.sum(np.square(p - c))))


