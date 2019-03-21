import numpy as np
import sys

def transpose(M):
    MT = np.zeros((M.shape[1], M.shape[0]), dtype=M.dtype)
    for i in range(0, M.shape[0]):
        for j in range(0, M.shape[1]):
            MT[j][i] = M[i][j]

    return MT

def transpose2(M):
    lst = []
    for i in range(M.shape[1]):
        lst.append(M[:,i])
    return np.array(lst)

def fast_transpose(M):
    return M.T

if __name__ == '__main__':
    M = np.random.normal(size=(20000, 20000))
#    print(M)

    if (sys.argv[1] == "2"):
        transpose2(M)
    elif (sys.argv[1] == "fast"):
        fast_transpose(M)
    else:
        transpose(M)
