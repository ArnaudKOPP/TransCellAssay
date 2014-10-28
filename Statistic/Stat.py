"""
Usefull definitions for some functions in project
"""

import numpy as np

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def kl(p, q):
    """
    Kullback-Leibler divergence D(P || Q) for discrete distributions

    or we can use scipy.stats.entropy with some parameters that became equal to that functions
    scipy.stats.entropy(pk, qk=None, base=None)
    If qk is not None, then compute a relative entropy (also known as Kullback-Leibler divergence or Kullback-Leibler
    distance) S = sum(pk * log(pk / qk), axis=0).

    Parameters
    ----------
    p, q : array-like, dtype=float, shape=n
        Discrete probability distributions.
    :param p: array
    :param q: array
    :return: distance
    """
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)

    return np.nansum(np.where(p != 0, p * np.log(p / q), 0))


def mad(arr):
    """
    Median Absolute Deviation: a "Robust" version of standard deviation.
    Indices variabililty of the sample.
    https://en.wikipedia.org/wiki/Median_absolute_deviation
    :param arr: numpy array value
    :return: return mad
    """
    try:
        # arr = np.ma.array(arr).compressed()  # should be faster to not use masked arrays.
        med = np.nanmedian(arr)
        return 1.4826 * np.nanmedian(np.absolute(arr - med))
    except Exception as e:
        print(e)


def ssmd(Array1, Array2):
    """
    Performed a SSMD on two polulations

    The larger the absolute value of SSMD between two populations, the greater the differentiation  between the two
    populations
    :param Array1: Must be equivalent of negative
    :param Array2: Must be equivalent of positive
    :return: SSMD Value
    """
    try:
        ssmd = (np.mean(Array2) - np.mean(Array1)) / (np.sqrt(np.abs(np.std(Array2) ** 2 - np.std(Array1) ** 2)))
        return ssmd
    except Exception as e:
        print(e)