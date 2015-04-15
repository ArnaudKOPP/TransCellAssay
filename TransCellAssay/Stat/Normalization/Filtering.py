# coding=utf-8
"""
Filtering data with given condition
"""

import numpy as np
import TransCellAssay as TCA
import logging

log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"


def plate_filtering(plate, channel, upper=None, lower=None, include=True, percent=False):
    """
    Make filtering of raw_data by condition
    :param plate: Plate object
    :param channel: on which channel to apply filtering
    :param upper: threshold that upper value will be erase
    :param lower: threshold that lower value will be erase
    :param include: include or not upper/lower value
    :param percent: Percent or value
    :return: filtered raw data
    """
    if not isinstance(plate, TCA.Plate):
        log.error('Plate object for input')
        raise TypeError
    else:
        log.info('Apply filtering on :{}'.format(plate.name))
        for key, values in plate.replica.items():
            plate[key] = __replica_filtering(values, channel, upper, lower, include, percent)
        return plate


def __replica_filtering(replica, channel, upper=None, lower=None, include=True, percent=False):
    log.debug('Apply filtering on :{}'.format(replica.name))
    replica.rawdata = __filtering_raw_data(replica.rawdata, channel, upper, lower, include, percent)
    return replica


def __filtering_raw_data(raw_data, channel, upper=None, lower=None, include=True, percent=False):
    if upper is not None:
        if percent:
            upper_threshold_value = np.percentile(raw_data.df[channel], upper)
            raw_data = __upper_filter_raw_data(raw_data, channel, upper_threshold_value, include)
        else:
            raw_data = __upper_filter_raw_data(raw_data, channel, upper, include)
    if lower is not None:
        if percent:
            lower_threshold_value = np.percentile(raw_data.df[channel], lower)
            raw_data = __lower_filter_raw_data(raw_data, channel, lower_threshold_value, include)
        else:
            raw_data = __lower_filter_raw_data(raw_data, channel, lower, include)
    raw_data._new_caching()
    return raw_data


def __upper_filter_raw_data(raw_data, channel, threshold, include):
    log.debug('Upper cut')
    if include:
        raw_data.df = raw_data.df[raw_data.df[channel] <= threshold]
    else:
        raw_data.df = raw_data.df[raw_data.df[channel] < threshold]
    return raw_data


def __lower_filter_raw_data(raw_data, channel, threshold, include):
    log.debug('Lower cut')
    if include:
        raw_data.df = raw_data.df[raw_data.df[channel] >= threshold]
    else:
        raw_data.df = raw_data.df[raw_data.df[channel] > threshold]
    return raw_data