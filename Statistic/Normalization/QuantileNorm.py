__author__ = 'Arnaud KOPP'
"""
QuantileNorm define method for normalizing a plate, replicat are quantile norm for giving them same distribution style
"""
import TCA
import numpy as np

# TODO change this function to take in input a dict of array
def PlateQuantNorm(plate, log=True):
    """
    anarray with samples in the columns and probes across the rows
    :param anarray:
    :return: return array
    """
    if isinstance(plate, TCA.Plate):
        if plate.getNumberReplicat() >= 2:
            return 0
        else:
            print('Non needs, only one replicat')
            return 0
    else:
        print('Take a Plate Object')
        raise TypeError


def quantile_normalization(anarray, log=True):
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