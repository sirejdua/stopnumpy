import numpy as np

def transpose(M):
    MT = np.zeros((M.shape[1], M.shape[0]), dtype=M.dtype)
    for i in range(0, M.shape[0]):
        for j in range(0, M.shape[1]):
            MT[j][i] = M[i][j]

    return MT

def fast_transpose(M):
    return M.T

