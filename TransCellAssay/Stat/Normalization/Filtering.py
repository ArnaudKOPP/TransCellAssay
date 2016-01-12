# coding=utf-8
"""
Filtering data with given condition
"""

import numpy as np
import TransCellAssay as TCA
import logging

log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def channel_filtering(plate, channel, value, thres="lower", include=True, percent=False):
    """
    Make filtering of raw_data by condition
    :param plate: Plate object
    :param channel: on which channel to apply filtering
    :param value: dict with key are rep name and items the cut_value for each replica
    :param thres: exclude lower or upper value
    :param include: include or not upper/lower value
    :param percent: Percent or value
    :return: filtered raw data
    """
    assert isinstance(plate, TCA.Plate)
    assert isinstance(value, dict)

    __valid_thres = ["lower", "upper"]
    assert thres in __valid_thres, "type must be {}".format(__valid_thres)

    log.info('Apply filtering on :{}'.format(plate.name))
    for key, values in plate:
        plate[key] = __replica_filtering(values, channel, thres, value[key], include, percent)
    return plate

def __replica_filtering(replica, channel, thres, cut_value, include=True, percent=False):
    log.debug('Apply filtering on :{}'.format(replica.name))
    replica.df = __filtering_raw_data(replica.df, channel, thres, cut_value, include, percent)
    replica._new_caching()
    return replica

def __filtering_raw_data(raw_data, channel, thres, value, include=True, percent=False):
    if percent:
        value = np.percentile(raw_data.df[channel], value)
    if thres == "upper":
        filtered = __upper_filter_raw_data(raw_data, channel, value, include)
    if thres == "lower":
        filtered = __lower_filter_raw_data(raw_data, channel, value, include)
    return filtered

def __upper_filter_raw_data(raw_data, channel, threshold, include):
    log.debug('Upper cut')
    if include:
        cutted = raw_data[raw_data[channel] <= threshold]
    else:
        cutted = raw_data[raw_data[channel] < threshold]
    return cutted

def __lower_filter_raw_data(raw_data, channel, threshold, include):
    log.debug('Lower cut')
    if include:
        cutted = raw_data[raw_data[channel] >= threshold]
    else:
        cutted = raw_data[raw_data[channel] > threshold]
    return cutted
