# coding=utf-8
"""
Rank Stat
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

import TransCellAssay as TCA
from scipy.stats import rankdata
import numpy as np


def rank_product(plate, SECdata=False, method="average", size=96, verbose=False):
    try:
        if isinstance(plate, TCA.Plate):
            rk_pdt = plate.PlateMap.platemap.values.flatten().reshape(size, 1)
            for key, value in plate.replicat.items():
                if SECdata:
                    rank = _get_data_rank(value.SECData, method=method)
                else:
                    rank = _get_data_rank(value.Data, method=method)
                rk_pdt = np.append(rk_pdt, rank.flatten().reshape(size, 1), axis=1)

            # rk_pdt = np.append(rk_pdt, np.mean(rk_pdt, axis=1).reshape(size, 1), axis=1)

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