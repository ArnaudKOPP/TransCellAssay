__author__ = 'Arnaud KOPP'
"""
NormPlate defined method for normalize plate, like remove edge effect or normalize between replicat
"""
import numpy as np

import Statistic.Normalization.MedianPolish as MedPol


def normalizeEdgeEffect(array):
    '''
    Apply a median polish for remove edge effect
    return residual matrix
    :param: array: a numpy array in matrix size
    :return: residual matrix
    '''
    try:
        mp = MedPol.MedianPolish(array)
        ge, ce, re, resid, tbl_org = mp.median_polish(100)
        print("median polish:")
        print("grand effect = ", ge)
        print("column effects = ", ce)
        print("row effects = ", re)
        print("-----Table of Residuals-------")
        print(resid)
        print("-----Original Table-------")
        print(tbl_org)

        ge, ce, re, resid, tbl_org = mp.median_polish(100, "average")
        print("average polish:")
        print("grand effect = ", ge)
        print("column effects = ", ce)
        print("row effects = ", re)
        print("-----Table of Residuals-------")
        print(resid)
        print("-----Original Table-------")
        print(tbl_org)
    except Exception as e:
        print(e)


# TODO change this function to take in input a dict of array
def quantile_normalization(anarray):
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


def normalizeBetweenReplicat(Plate):
    '''
    Apply a norm between replicat
    :return:
    '''
    try:
        if (Plate.replicat.getNBreplicat()) < 2:
            print('Can\'t apply this normalization because under two replicats, need at least two replicats ')
        else:
            print('Normalization not yet implemented')
    except Exception as e:
        print(e)


