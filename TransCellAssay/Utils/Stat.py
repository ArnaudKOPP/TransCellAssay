# coding=utf-8
"""
Usefull definitions for some functions in project
"""

import numpy as np
from numpy import mean, absolute, math
import scipy.stats
import pandas as pd

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def quantile_normalization(anarray):
    """
    an array with samples in the columns and probes across the rows
    """
    A=anarray
    AA = np.zeros_like(A)
    I = np.argsort(A,axis=0)
    AA[I,np.arange(A.shape[1])] = np.mean(A[I,np.arange(A.shape[1])],axis=1)[:,np.newaxis]
    return AA


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


def CohenEffectSize(group1, group2):
    """
    Determine Effect size
    Cohen's d statistic : compare the difference between groups to the variability
    within groups
    """
    diff = group1.var()

    var1 = group1.var()
    var2 = group2.var()
    n1, n2 = len(group1), len(group2)

    pooled_var = (n1 * var1 + n2 * var2) / (n1 + n2)
    d = diff / math.sqrt(pooled_var)
    return d


def Covariance(xs, ys, meanx=None, meany=None):
    """
    Covariance is a measure of the tendency of two variables to vary together.
    positive when the deviations have the same sign and negative when they have the
    opposite sign.
    """
    xs = np.asarray(xs)
    ys = np.asarray(ys)

    if meanx is None:
        meanx = np.mean(xs)
    if meany is None:
        meany = np.mean(ys)

    cov = np.dot(xs-meanx, ys-meany) / len(xs)
    return cov


def mad2(data, axis=None):
    return mean(absolute(data - mean(data, axis)), axis)


def mad(arr):
    """
    Median Absolute Deviation: a "Robust" version of standard deviation.
    Indices variabililty of the sample.
    https://en.wikipedia.org/wiki/Median_absolute_deviation
    :param arr: numpy array value
    :return: return mad
    """
    # arr = np.ma.array(arr).compressed()  # should be faster to not use masked arrays.
    med = np.nanmedian(arr)
    return 1.4826 * np.nanmedian(np.absolute(arr - med))


def ssmd(array1, array2):
    """
    Performed a SSMD on two polulations

    The larger the absolute value of SSMD between two populations, the greater the differentiation  between the two
    populations
    :param array1: Must be equivalent of negative
    :param array2: Must be equivalent of positive
    :return: SSMD Value
    """
    ssmd = (np.mean(array2) - np.mean(array1)) / (np.sqrt(np.abs(np.std(array2) ** 2 - np.std(array1) ** 2)))
    return ssmd


def mann_whitney(array1, array2):
    """

    :param array1:
    :param array2:
    :return:
    """
    import scipy.stats
    u, prob = scipy.stats.mannwhitneyu(array1, array2)
    return u, prob


def wilcoxon_rank_sum(array1, array2):
    """

    :param array1:
    :param array2:
    :return:
    """
    import scipy.stats
    z, p = scipy.stats.ranksums(array1, array2)
    return z, p


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
    mean1 = np.nanmean(array)
    std = np.nanstd(array)
    norm = np.zeros(array.shape)

    for i in range(0, len(array) - 1, 1):
        norm[i] = (array[i] - mean1) / std

    a = __asquare(norm)
    return a


def __asquare(data):
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


def __cdf(y, mu, varb):
    res = 0.5 * (1 + scipy.stats.norm.cdf((y - mu) / varb))
    return res


def percentile_based_outlier(data, threshold=95):
    """
    Based on percentile determine outliers
    :param data:
    :param threshold:
    :return:
    """
    diff = (100 - threshold) / 2.0
    minval, maxval = np.percentile(data, [diff, 100 - diff])
    return (data < minval) | (data > maxval)


# theory behind this : http://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm
def outlier_mad_based(data, thresh=2):
    """
    Based on mad, determine outliers by row
    :param data:
    :param thresh:
    :return: true for 'correct' value, false for outlier
    """
    if isinstance(data, pd.Series):
        data = data.values
    if isinstance(data, pd.DataFrame):
        data = data.values
    or_shape = data.shape
    data = data.flatten()
    if len(data.shape) == 1:
        data = data[:, None]
    median = np.median(data, axis=0)
    diff = np.sum((data - median) ** 2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)
    modified_z_score = 0.6745 * diff / med_abs_deviation
    modified_z_score = modified_z_score.reshape(or_shape)
    return modified_z_score > thresh


def without_outlier_mad_based(data, thresh=2):
    """
    Based on mad, determine outliers by row
    :param data:
    :param thresh:
    :return: true for 'correct' value, false for outlier
    """
    if isinstance(data, pd.Series):
        data = data.values
    if isinstance(data, pd.DataFrame):
        data = data.values
    or_shape = data.shape
    data = data.flatten()
    if len(data.shape) == 1:
        data = data[:, None]
    median = np.median(data, axis=0)
    diff = np.sum((data - median) ** 2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)
    modified_z_score = 0.6745 * diff / med_abs_deviation
    modified_z_score = modified_z_score.reshape(or_shape)
    return modified_z_score < thresh


def outlier_std_based(data, thresh=2):
    """
    Based on mad, determine outliers by row
    :param data:
    :param thresh:
    :return: true for 'correct' value, false for outlier
    """
    if isinstance(data, pd.Series):
        data = data.values
    if isinstance(data, pd.DataFrame):
        data = data.values
    or_shape = data.shape
    data = data.flatten()
    if len(data.shape) == 1:
        data = data[:, None]
    mean = np.mean(data, axis=0)
    diff = np.sum((data - mean) ** 2, axis=-1)
    diff = np.sqrt(diff)
    std = np.std(diff)
    modified_z_score = 0.6745 * diff / std
    modified_z_score = modified_z_score.reshape(or_shape)
    return modified_z_score > thresh


def without_outlier_std_based(data, thresh=2):
    """
    Based on mad, determine outliers by row
    :param data:
    :param thresh:
    :return: true for 'correct' value, false for outlier
    """
    if isinstance(data, pd.Series):
        data = data.values
    if isinstance(data, pd.DataFrame):
        data = data.values
    or_shape = data.shape
    data = data.flatten()
    if len(data.shape) == 1:
        data = data[:, None]
    mean = np.mean(data, axis=0)
    diff = np.sum((data - mean) ** 2, axis=-1)
    diff = np.sqrt(diff)
    std = np.std(diff)
    modified_z_score = 0.6745 * diff / std
    modified_z_score = modified_z_score.reshape(or_shape)
    return modified_z_score < thresh


def doubleMADsfromMedian(y,thresh=3.5):
    # warning: this function does not check for NAs
    # nor does it address issues when
    # more than 50% of your data have identical values
    m = np.median(y)
    abs_dev = np.abs(y - m)
    left_mad = np.median(abs_dev[y<=m])
    right_mad = np.median(abs_dev[y>=m])
    y_mad = np.zeros(len(y))
    y_mad[y < m] = left_mad
    y_mad[y > m] = right_mad
    modified_z_score = 0.6745 * abs_dev / y_mad
    modified_z_score[y == m] = 0
    return modified_z_score > thresh
