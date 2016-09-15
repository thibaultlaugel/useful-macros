import pandas as pd
import numpy as np
import random
from random import randrange, choice
from sklearn.neighbors import NearestNeighbors

def SMOTE(T, N, k=5):
    """
    Returns (N/100) * n_minority_samples synthetic minority samples.
    Parameters
    ----------
    T : array-like, shape = [n_minority_samples, n_features]
        Holds the minority samples
    N : percetange of new synthetic samples:
        n_synthetic_samples = N/100 * n_minority_samples. Can be < 100.
    k : int. Number of nearest neighbours.
    Returns
    -------
    S : Synthetic samples. array,
        shape = [(N/100) * n_minority_samples, n_features].
    """
    n_minority_samples, n_features = T.shape

    if N < 100:
        print('if N is less than 100%, randomize the minority class samples as only a random percent of them will be SMOTEd.')
        idx_picked = np.random.choice(range(n_minority_samples), size=N/100)
        T = T[idx_picked, :]
        N = 100

    if (N % 100) != 0:
        raise ValueError("N must be < 100 or multiple of 100")

    N = int(N/100)
    n_synthetic_samples = N * n_minority_samples
    S = np.zeros(shape=(n_synthetic_samples, n_features))

    kNN = NearestNeighbors(n_neighbors = k)
    kNN.fit(T)

    new_index = 0

    for i in range(n_minority_samples):
        nn = kNN.kneighbors(T[i], return_distance=False)
        for n in range(N): #nn includes T[i], we don't want to select it so we pick again if we pick it
            nn_index = np.random.choice(nn[0][1:])
            for col_idx in range(n_features):
                dif = T[nn_index, col_idx] - T[i, col_idx]
                gap = np.random.uniform(low=0.0, high=1.0)
                '''gap: definition pb? --> original paper states that a new random nb is picked for every col (synthetic sample is in a "cube" defined by T[i] and its neighbor)
                however implementations often use the same random nb for all colls (synthetic sample is on the "segment" defined by T[i] and its neighbor)
                '''
                S[new_index, col_idx] = S[i, col_idx] + gap * dif
            new_index += 1
    return S
