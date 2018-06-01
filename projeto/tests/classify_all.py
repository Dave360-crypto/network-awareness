import numpy as np
import sys, os
import asyncio
import websockets, json
from classifier.neuronalNetworks.classify_neuronalNetworks import classify_neuronalNetworks

sys.path.append("..")

from classifier.utils.classify import extractFeatures, extractFeaturesWavelet, extractFeaturesSilence, breakData
from classifier.vector.classify_vector import classify_vector
from classifier.vectorPCA.classify_vectorPCA import classify_vectorPCA
from classifier.multivariatePCA.classify_multivariatePCA import classify_multivaritePCA
from classifier.distances.classify_distances import classify_distances
from classifier.clustering.classify_clustering import classify_clustering


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "classifier/data/")

WINDOW = 120

if __name__ == '__main__':
    # classify unknown data
    unknown_data = np.loadtxt(DATA_PATH + 'mining_download_upload_bytes.dat')

    # break data
    break_data = breakData(unknown_data, oWnd=WINDOW)

    # extract features of the unknown break data
    features_data = extractFeatures(break_data)[0]
    features_dataS = extractFeaturesSilence(break_data)[0]
    features_dataW = extractFeaturesWavelet(break_data)[0]
    unknown_data_features = np.hstack((features_data, features_dataS, features_dataW))

    # creating train and test data for each Class (YouTube, Browsing and Mining)
    # based on vector
    classify_vector(unknown_data_features, printing=True)

    # based on vector PCA
    classify_vectorPCA(unknown_data_features, printing=True)

    # based on multivariate PCA
    classify_multivaritePCA(unknown_data_features, printing=True)

    # based on distances
    classify_distances(unknown_data_features, printing=True)

    #based on clustering (Kmeans)
    classify_clustering(unknown_data_features, printing=True)

    # based on neural networks
    classify_neuronalNetworks, nObsTest = classify_neuronalNetworks(unknown_data_features, printing=True)

    list = []
    async def data(websocket, path):
        for key, value in classify_neuronalNetworks:
            list.append(str(int(value / nObsTest * 100)))

        await websocket.send(json.dumps(list))

    start_server = websockets.serve(data, '127.0.0.1', 1234)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()







