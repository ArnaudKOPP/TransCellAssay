__author__ = 'Arnaud KOPP'

import TCA
import Statistic.Normalization
import numpy as np
from scipy import stats


def SystematicErrorDetectionTest(Object, save=True):
    '''
    Search for systematic error in plate or replicat
    :param Plate:
    :return:
    '''
    try:
        if isinstance(Object, TCA.Plate):
            print("Plate SEDT")
            if Object.DataMatrixMean or Object.DataMatrixMedian is None:
                print("Launch computeDataMatrixFromReplicat First")
                raise ValueError

        # col of numpy array : array[:,x]
        # row of numpy array : array[x,:]
        if isinstance(Object, TCA.Replicat):
            print("Replicat SEDT")
            if Object.DataMatrixMean or Object.DataMatrixMedian is None:
                print("Launch computeDataMatrixForFeature First")
                raise ValueError
        else:
            raise TypeError
    except Exception as e:
        print(e)


def TTest(Array1, Array2, alpha=0.05):
    '''
    Compute a T Test on two array
    In this test, the nul hypothesis H0 was the selected row/col does not contain systematic error
    This test, also known as Welch's t-test, is used only when the two population variances are not assumed to be equal
    (the two sample sizes may or may not be equal) and hence must be estimated separately.
    if T-stat is > than value from table with alpha and dof, then not systematic error bacause we accept H0 hypothesis
    :param Array1: Row or Col from matrix
    :param Array2: All remaining measurement
    :return:
    '''
    try:
        N1 = Array1.size
        N2 = Array2.size
        tstat = (np.mean(Array1) - np.mean(Array2)) / (np.sqrt((np.var(Array1) / N1) + (np.var(Array2) / N2)))
        dof = ((np.var(Array1) / N1) + (np.var(Array2) / N2)) ** 2 / (
            ((np.var(Array1) / N1) ** 2 / (N1 - 1)) + ((np.var(Array2) / N2) ** 2 / (N2 - 1)))
        theo = stats.t.isf(alpha, dof)
        if tstat > theo:
            print("No systematic Error")
        else:
            print("Systematic Error")
        return tstat, dof
    except Exception as e:
        print(e)