# coding=utf-8
"""
Usefull definitions for some functions in project
"""

import numpy as np
import scipy.stats

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
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


def ssmd(array1, array2):
    """
    Performed a SSMD on two polulations

    The larger the absolute value of SSMD between two populations, the greater the differentiation  between the two
    populations
    :param array1: Must be equivalent of negative
    :param array2: Must be equivalent of positive
    :return: SSMD Value
    """
    try:
        ssmd = (np.mean(array2) - np.mean(array1)) / (np.sqrt(np.abs(np.std(array2) ** 2 - np.std(array1) ** 2)))
        return ssmd
    except Exception as e:
        print(e)


def mann_whitney(array1, array2):
    """

    :param array1:
    :param array2:
    :return:
    """
    try:
        import scipy.stats

        u, prob = scipy.stats.mannwhitneyu(array1, array2)
        return u, prob
    except Exception as e:
        print(e)


def wilcoxon_rank_sum(array1, array2):
    """

    :param array1:
    :param array2:
    :return:
    """
    try:
        import scipy.stats

        z, p = scipy.stats.ranksums(array1, array2)
        return z, p
    except Exception as e:
        print(e)


def adjustpvalues(pvalues, method='fdr', n=None):
    """
    returns an array of adjusted pvalues
    Reimplementation of p.adjust in the R package.
    For more information, see the documentation of the
    p.adjust method in R.

    :param pvalues: numeric vector of p-values (possibly with 'NA's).
    :param method: correction method. Valid values are: : fdr, bonferroni, holm, hochberg, BH or BY
    :param n: number of comparisons, must be at least 'length(p)'; only set
    this (to non-default) when you know what you are doing
    """

    if n is None:
        n = len(pvalues)

    if method == "fdr":
        method = "BH"

    # optional, remove NA values
    p = np.array(pvalues, dtype=np.float)
    lp = len(p)

    assert n <= lp

    if n <= 1:
        return p

    if method == "bonferroni":
        p0 = n * p
    elif method == "holm":
        i = np.arange(lp)
        o = np.argsort(p)
        ro = np.argsort(o)
        m = np.maximum.accumulate((n - i) * p[o])
        p0 = m[ro]
    elif method == "hochberg":
        i = np.arange(0, lp)[::-1]
        o = np.argsort(1 - p)
        ro = np.argsort(o)
        m = np.minimum.accumulate((n - i) * p[o])
        p0 = m[ro]
    elif method == "BH":
        i = np.arange(1, lp + 1)[::-1]
        o = np.argsort(1 - p)
        ro = np.argsort(o)
        m = np.minimum.accumulate(float(n) / i * p[o])
        p0 = m[ro]
    elif method == "BY":
        i = np.arange(1, lp + 1)[::-1]
        o = np.argsort(1 - p)
        ro = np.argsort(o)
        q = np.sum(1.0 / np.arange(1, n + 1))
        m = np.minimum.accumulate(q * float(n) / i * p[o])
        p0 = m[ro]
    elif method == "none":
        p0 = p

    return np.minimum(p0, np.ones(len(p0)))


def anderson_darling_test(array):
    """
    The Anderson–Darling test is a statistical test of whether a given sample of data is drawn from a given probability
    distribution.
    :param array:
    :return: return value
    """
    try:
        mean1 = np.nanmean(array)
        std = np.nanstd(array)
        norm = np.zeros(array.shape)

        for i in range(0, len(array) - 1, 1):
            norm[i] = (array[i] - mean1) / std

        a = __asquare(norm)
        return a
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)


def __asquare(data):
    try:
        mean1 = np.nanmean(data)
        varianceb = np.sqrt(2 * np.nanvar(data))
        err = 0
        cpt = 0
        for i in range(0, len(data) - 1, 1):
            cpt += 1
            err += ((2 * cpt - 1) * np.log(__cdf(data[i], mean1, varianceb)) + np.log(
                1 - __cdf(data[len(data - 1 - i)], mean1, varianceb)))
        a = -len(data) - err / len(data)

        return a
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)


def __cdf(y, mu, varb):
    try:
        res = 0.5 * (1 + scipy.stats.norm.cdf((y - mu) / varb))
        return res
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)


def t_test(array1, array2):
    """
    Compute a T Test on two array
    In this test, the nul hypothesis H0 was the selected row/col does not contain systematic error
    This test, also known as Welch's t-test, is used only when the two population variances are not assumed to be equal
    (the two sample sizes may or may not be equal) and hence must be estimated separately.
    if T-stat is > than value from table with alpha and dof, then not systematic error because we accept H0 hypothesis
    :param array1: Row or Col from matrix
    :param array2: All remaining measurement
    :return: tstat and degree of freedom
    """
    try:
        n1 = array1.size
        n2 = array2.size
        tstat = (np.mean(array1) - np.mean(array2)) / (np.sqrt((np.var(array1) / n1) + (np.var(array2) / n2)))
        dof = ((np.var(array1) / n1) + (np.var(array2) / n2)) ** 2 / (
            ((np.var(array1) / n1) ** 2 / (n1 - 1)) + ((np.var(array2) / n2) ** 2 / (n2 - 1)))
        return tstat, dof
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)


def ttest(array1, array2, alpha=0.05):
    """
    Compute a T Test on two array
    In this test, the nul hypothesis H0 was the selected row/col does not contain systematic error
    This test, also known as Welch's t-test, is used only when the two population variances are not assumed to be equal
    (the two sample sizes may or may not be equal) and hence must be estimated separately.
    if T-stat is > than value from table with alpha and dof, then not systematic error because we accept H0 hypothesis
    :param array1: Row or Col from matrix
    :param array2: All remaining measurement
    :param alpha: alpha
    :return: True if Systematic error is present or False
    """
    try:
        n1 = array1.size
        n2 = array2.size
        tstat = (np.mean(array1) - np.mean(array2)) / (np.sqrt((np.var(array1) / n1) + (np.var(array2) / n2)))
        dof = ((np.var(array1) / n1) + (np.var(array2) / n2)) ** 2 / (
            ((np.var(array1) / n1) ** 2 / (n1 - 1)) + ((np.var(array2) / n2) ** 2 / (n2 - 1)))
        theo = scipy.stats.t.isf(alpha, dof)
        if tstat > theo:
            return True
        else:
            return False
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)