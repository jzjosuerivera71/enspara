from cython import boundscheck

import numpy as np
cimport numpy as np

@boundscheck(False)
def euclidean_distance(double[:, :] X, double[:] Y):
    '''
    Computes the euclidean distance between a 2d array of doubles (`X`)
    and a 1d array of doubles (`Y`), which has dimensions of a column in
    `X`. This function computes the euclidean distance between them.

    This implementation has ~2/3 of the runtime of the sklearn function
    of the same name (although it has a slightly different function
    signature.)
    '''

    dists = np.einsum('ij,ij->i', X, X)
    dists += np.dot(Y, Y)
    dists -= 2*np.dot(X, Y)
    
    # numerical instability sometimes makes near-zero distances a small
    # negative number here.
    dists[dists < 0] = 0
        
    return np.array(np.sqrt(dists))
