"""Fingerprint-accepting and sparse matrix version of the JVHW entropy
estimator.

Chuan-Zheng Lee
EE378A project: Fundamental limits in language modeling
June 2017
"""

import numpy as np
import scipy.io as sio
import scipy.sparse as ssp
from est_entro import entro_mat

poly_entro = None

def est_entro_JVHW_from_fingerprint_dict(fingerprint):
    """`fingerprint` should be a dict mapping frequencies to how often that
    frequency occurs in the profile."""

    fingerprint = {(k if isinstance(k, tuple) else (k,0)): v for k, v in fingerprint.items()}
    shape = tuple(np.max(np.array(list(fingerprint.keys())), axis=0) + 1)
    f_dok = ssp.dok_matrix(shape, dtype=int)
    n = 0
    for k, v in fingerprint.items():
        f_dok[k] = v
        if k[1] == 0: # assume all columns imply the same n as the first
            n += (k[0] + 1) * v
    wid = f_dok.shape[1]

    order = min(4 + int(np.ceil(1.2 * np.log(n))), 22)
    global poly_entro
    if poly_entro is None:
        poly_entro = sio.loadmat('poly_coeff_entro.mat')['poly_entro']
    coeff = poly_entro[order-1, 0][0]

    f_csc = f_dok.tocsc()
    fnonzero_rows = sorted(list(set(f_csc.nonzero()[0])))

    prob_dok = ssp.dok_matrix((f_csc.shape[0], 1))
    prob_dok[fnonzero_rows,0] = (np.array(fnonzero_rows, dtype=float, ndmin=2).T+1)/n
    prob_csc = prob_dok.tocsc()

    # Piecewise linear/quadratic fit of c_1
    V1 = np.array([0.3303, 0.4679])
    V2 = np.array([-0.530556484842359, 1.09787328176926, 0.184831781602259])
    f_row1 = f_csc[0].toarray().squeeze(0)
    f1nonzero = f_row1 > 0
    c_1 = np.zeros(wid)

    with np.errstate(divide='ignore', invalid='ignore'):
        if n >= order and f1nonzero.any():
            if n < 200:
                c_1[f1nonzero] = np.polyval(V1, np.log(n / f[0, f1nonzero]))
            else:
                n2f1_small = f1nonzero & (np.log(n / f_row1) <= 1.5)
                n2f1_large = f1nonzero & (np.log(n / f_row1) > 1.5)
                c_1[n2f1_small] = np.polyval(V2, np.log(n / f_row1[n2f1_small]))
                c_1[n2f1_large] = np.polyval(V1, np.log(n / f_row1[n2f1_large]))

            # make sure nonzero threshold is higher than 1/n
            c_1[f1nonzero] = np.maximum(c_1[f1nonzero], 1 / (1.9 * np.log(n)))

        prob_mat = ssp.dok_matrix(f_csc.shape)
        prob_mat[fnonzero_rows] = entro_mat(prob_csc.data, n, coeff, c_1)

    return np.array(f_csc.multiply(prob_mat).sum(axis=0)).squeeze() / np.log(2)
