__author__ = 'Arnaud KOPP'

from scipy import stats
import numpy as np


def t_test(Array1, Array2):
    '''
    Compute a T Test on two array
    In this test, the nul hypothesis H0 was the selected row/col does not contain systematic error
    This test, also known as Welch's t-test, is used only when the two population variances are not assumed to be equal
    (the two sample sizes may or may not be equal) and hence must be estimated separately.
    if T-stat is > than value from table with alpha and dof, then not systematic error because we accept H0 hypothesis
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
        return tstat, dof
    except Exception as e:
        print(e)


def TTest(Array1, Array2, alpha=0.05):
    '''
    Compute a T Test on two array
    In this test, the nul hypothesis H0 was the selected row/col does not contain systematic error
    This test, also known as Welch's t-test, is used only when the two population variances are not assumed to be equal
    (the two sample sizes may or may not be equal) and hence must be estimated separately.
    if T-stat is > than value from table with alpha and dof, then not systematic error because we accept H0 hypothesis
    :param Array1: Row or Col from matrix
    :param Array2: All remaining measurement
    :param alpha: alpha
    :return: True if Systematic error is present or False
    '''
    try:
        N1 = Array1.size
        N2 = Array2.size
        tstat = (np.mean(Array1) - np.mean(Array2)) / (np.sqrt((np.var(Array1) / N1) + (np.var(Array2) / N2)))
        dof = ((np.var(Array1) / N1) + (np.var(Array2) / N2)) ** 2 / (
            ((np.var(Array1) / N1) ** 2 / (N1 - 1)) + ((np.var(Array2) / N2) ** 2 / (N2 - 1)))
        theo = stats.t.isf(alpha, dof)
        if tstat > theo:
            return True
        else:
            return False
    except Exception as e:
        print(e)