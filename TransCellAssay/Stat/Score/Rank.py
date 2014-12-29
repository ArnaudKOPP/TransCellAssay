"""
Rank Stat
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"

import TransCellAssay as TCA
from scipy.stats import rankdata
import numpy as np


def getRankStat(plate, SECdata=False, method="average", size=96):
    # TODO implement this class
    try:
        if isinstance(plate, TCA.Plate):
            name = plate.PlateMap.platemap.values.flatten().reshape(size, 1)
            for key, value in plate.replicat:
                if SECdata:
                    rank = _get_data_rank(value.SECdata, method=method)
                    name = np.append(name, rank.flatten().reshape(size, 1), axis=1)
                else:
                    rank = _get_data_rank(value.Data, method=method)
                    name = np.append(name, rank.flatten().reshape(size, 1), axis=1)

            name = np.append(np.mean(name, axis=1).reshape(size, 1), axis=1)
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