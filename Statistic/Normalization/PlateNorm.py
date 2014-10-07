__author__ = 'Arnaud KOPP'
"""
PlateNorm define method for normalizing a plate, replicat are quantile norm for giving them same distribution style
zscore Transformation and not log transformation by default
"""
import TCA
import numpy as np

ndtri = None


def PlateNorm(plate, feature, zscore=True, log=True):
    """
    Normalized a Plate object, in first apply a log2 transformation, then apply a quantile normalization, and
    for finish appyly a score transformation
    :param anarray:
    :return: return array
    """
    if isinstance(plate, TCA.Plate):
        if plate.getNumberReplicat() >= 2:
            PlateData = plate.getAllDataFromReplicat(feature)

        else:
            print('No needs, only one replicat')
            return 0
    else:
        print('Take a Plate Object')
        raise TypeError

def zscoreTransformation(array):
    """
    Z score Transformation
    :param array: input of Well
    :return: return array
    """
    return (array - array.mean())/array.std(ddof=0)


def quantile_normalization(anarray, log):
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


