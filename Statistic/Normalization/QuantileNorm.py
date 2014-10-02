__author__ = 'Arnaud KOPP'
"""
NormPlate defined method for normalize plate, like remove edge effect or normalize between replicat
"""
import numpy as np

# TODO change this function to take in input a dict of array
def quantile_normalization(anarray, log=False):
    """
    anarray with samples in the columns and probes across the rows
    :param anarray:
    :return: return array
    """
    try:
        A = anarray
        AA = np.zeros_like(A)
        I = np.argsort(A, axis=0)
        AA[I, np.arange(A.shape[1])] = np.mean(A[I, np.arange(A.shape[1])], axis=1)[:, np.newaxis]
        return AA
    except Exception as e:
        print(e)
