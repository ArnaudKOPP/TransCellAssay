# coding=utf-8
"""
The rank product is a biologically motivated test for the detection of differentially expressed genes
http://docs.scipy.org/doc/scipy-dev/reference/generated/scipy.stats.rankdata.html
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

import TransCellAssay as TCA
from scipy.stats import rankdata
import numpy as np


def rank_product(plate, secdata=False, mean_method="mean", rank_method="average", size=96, verbose=False):
    """
    Compute the rank product of plate with replicat data
    :param plate: plate object
    :param secdata: use or not systematic error corrected data
    :param mean_method: mean or median for rank product
    :param rank_method: method for rank : average, min, max, dense, ordinal
    :param size: number of well of plate
    :param verbose: print or not result
    :return: return np ndarray with result
    """
    try:
        if isinstance(plate, TCA.Plate):
            rk_pdt = plate.platemap.platemap.values.flatten().reshape(size, 1)
            for key, value in plate.replica.items():
                if secdata:
                    rank = _get_data_rank(value.sec_array, method=rank_method)
                else:
                    rank = _get_data_rank(value.array, method=rank_method)
                rk_pdt = np.append(rk_pdt, rank.flatten().reshape(size, 1), axis=1)

            if mean_method is 'mean':
                rk_pdt = np.append(rk_pdt, np.mean(rk_pdt[:, 1:], axis=1).reshape(size, 1), axis=1)
            elif mean_method is 'median':
                rk_pdt = np.append(rk_pdt, np.median(rk_pdt[:, 1:], axis=1).reshape(size, 1), axis=1)

            if verbose:
                print(rk_pdt)
            return rk_pdt
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _get_data_rank(array, method="average"):
    """
    Take in input a numpy array and return rank data in same shape
    :param array: numpy array to get rank
    :param method: average (default, min, max, dense or ordinal
    :return: return rank in same shape as array input
    """
    try:
        if isinstance(array, np.ndarray):
            org_shape = array.shape
            rank_matrix = rankdata(array, method=method)
            return rank_matrix.reshape(org_shape)
        else:
            raise TypeError
    except Exception as e:
        print(e)