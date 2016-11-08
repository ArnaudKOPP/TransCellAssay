# coding=utf-8
"""
The rank product is a biologically motivated test for the detection of differentially expressed genes
http://docs.scipy.org/doc/scipy-dev/reference/generated/scipy.stats.rankdata.html
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"

import TransCellAssay as TCA
import pandas as pd
from scipy.stats import rankdata
import numpy as np
import logging
log = logging.getLogger(__name__)


def rank_product(plate, chan, secdata=False, mean_method="mean", rank_method="average"):
    """
    Compute the rank product of plate with replica data
    :param plate: plate object
    :param chan: On which Channel get Rank
    :param secdata: use or not systematic error corrected data
    :param mean_method: mean or median for rank product
    :param rank_method: method for rank : average, min, max, dense, ordinal
    :return: return np ndarray with result
    """
    assert isinstance(plate, TCA.Plate)
    __SIZE__ = len(plate.platemap.platemap.values.flatten())

    if plate._array_channel != chan:
        plate.agg_data_from_replica_channel(channel=chan, forced_update=True)

    log.info('Perform Rank product on plate : {0} over channel {1}'.format(plate.name, chan))

    x = pd.DataFrame(plate.platemap.platemap.values.flatten().reshape(__SIZE__, 1), columns=['PlateMap'])
    for key, value in plate.replica.items():
        log.debug('Rank : iteration on %s' % value.name)
        if secdata:
            rank = __get_data_rank(value.array_c, method=rank_method)
        else:
            rank = __get_data_rank(value.array, method=rank_method)
        x[value.name+'_Rank'] = rank.flatten().reshape(__SIZE__ , 1)

    if mean_method is 'mean':
        x['Mean Rank'] = np.mean(x.iloc[:, 1:], axis=1).reshape(__SIZE__ , 1)
    elif mean_method is 'median':
        x['Median Rank'] = np.median(x.iloc[:, 1:], axis=1).reshape(__SIZE__ , 1)

    return x


def __get_data_rank(array, method="average"):
    """
    Take in input a numpy array and return rank data in same shape
    :param array: numpy array to get rank
    :param method: average (default, min, max, dense or ordinal
    :return: return rank in same shape as array input
    """
    if method not in ['average', 'min', 'max', 'dense', 'ordinal']:
        raise ValueError('Wrong rank method')
    org_shape = array.shape
    rank_matrix = rankdata(array, method=method)
    return rank_matrix.reshape(org_shape)
