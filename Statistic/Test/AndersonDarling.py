__author__ = 'Arnaud KOPP'
'''
The Anderson–Darling test is a statistical test of whether a given sample of data is drawn from a given probability
distribution.
'''
import numpy as np
import scipy.stats


def Anderson_Darling(Array):
    try:
        Mean1 = np.nanmean(Array)
        STD = np.nanstd(Array)
        norm = np.zeros(Array.shape)

        for i in range(0, len(Array) - 1, 1):
            norm[i] = (Array[i] - Mean1) / STD

        A = Asquare(norm)
        return A
    except Exception as e:
        print(e)


def Asquare(data):
    try:
        mean1 = np.nanmean(data)
        varianceb = np.sqrt(2 * np.nanvar(data))
        err = 0
        cpt = 0
        for i in range(0, len(data) - 1, 1):
            cpt += 1
            err += ((2 * cpt - 1) * np.log(CDF(data[i], mean1, varianceb)) + np.log(
                1 - CDF(data[len(data - 1 - i)], mean1, varianceb)))
        A = -len(data) - err / len(data)

        return A
    except Exception as e:
        print(e)


def CDF(y, mu, varb):
    try:
        Res = 0.5 * (1 + scipy.stats.norm.cdf((y - mu) / varb))
        return Res
    except Exception as e:
        print(e)