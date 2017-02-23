# coding=utf-8
"""
Controls based normalization : Percent Of Control and Normalized percent of inhibition
Non controls based normalization : Percent of Sample, Robust Percent of Sample, Z-score and robust Z-score

Use this with caution, if you want to keep some event with 0 in value, don't normalize with log transformation

Add Feature Scaling normalization :
http://en.wikipedia.org/wiki/Feature_scaling
"""

import numpy as np
import pandas as pd
import TransCellAssay as TCA
from TransCellAssay.Utils.Stat import mad
import logging
log = logging.getLogger(__name__)


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2017 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def plate_feature_scaling(plate, channel, mean_scaling=False):
    """
    Apply feature scaling on plate object across all replica
    channel Scaling to [0,1] or [0, mean of max] if mean_scaling is True
    :param plate: Plate object
    :param channel: Which channel to scale
    :param mean_scaling: if True, the max is the mean of max across all replica (instead of 1)
    """
    try:
        assert isinstance(plate, TCA.Plate)
        log.debug('Perform feature scaling on {}'.format(plate.name))
        min_lst = []
        max_lst = []

        # search min and max across all replica
        for key, value in plate:
            min_lst.append(np.min(value.df[channel].values))
            max_lst.append(np.max(value.df[channel].values))

        # apply channel scaling across all replica
        for key, value in plate:
            value = __df_scaling(value, min_lst, max_lst, channel, mean_scaling)
            value.isNormalized = True

        plate.isNormalized = True
    except Exception as e:
        print(e)


def __df_scaling(replica, min_val, max_val, channel, mean=False):
    """
    Apply feature scalling on replica rawdata
    :param replica: replica object
    :param min_val: min val for inf limit
    :param max_val: max val for sup limit
    :param channel: which channel to work
    :param mean: bool
    :return: normalized raw data
    """
    assert isinstance(replica, TCA.Replica)
    replica.df.loc[:, channel] = (replica.df.loc[:, channel] - min(min_val)) / (max(max_val) - min(min_val))
    if mean:
        replica.df.loc[:, channel] *= (sum(max_val) / len(max_val))
    return replica


def rawdata_variability_normalization(obj, channel, method=None, log2_transf=True, neg_control=None, pos_control=None,
                                      threshold=None):
    """
    Take a dataframe from replica object and apply desired strategy of variability normalization
    :param obj: Plate or replica object
    :param channel: on which channel to normalize
    :param method: which method to apply
    :param log2_transf: apply log2 transformation
    :param neg_control: list of well for negative control A1 A2 ...
    :param pos_control: list of well for positive control A1 A2 ...
    :param threshold: used in background subtraction (median is 50) you can set as you want
    :return: normalized data
    """
    try:
        __valid_method = ['Zscore', 'RobustZscore', 'PercentOfSample', 'RobustPercentOfSample', 'PercentOfControl',
                          'RobustPercentOfControl', 'NormalizedPercentInhibition', 'BackgroundSubstraction', None]

        if method not in __valid_method:
            raise ValueError("Method don't exist, choose : {}".format(__valid_method))

        # check if channel is list
        if isinstance(channel, list):
            raise NotImplementedError("Multiple channels normalization don't implemented, use class functions")

        if isinstance(obj, TCA.Plate):
            for key, value in obj:
                value = __rd_norm(value, channel, method, log2_transf, neg_control, pos_control,
                                             threshold)
            log.info('Plate {} : RawData normalization on channel {}'.format(obj.name, channel))
        elif isinstance(obj, TCA.Replica):
            obj = __rd_norm(obj, channel, method, log2_transf, neg_control, pos_control,
                                       threshold)
            log.info('Replica {} : RawData normalization on channel {}'.format(obj.name, channel))
        else:
            raise TypeError("Don't take this object, only Plate or Replica")
    except Exception as e:
        print(e)


def __rd_norm(replica, channel, method=None, log2_transf=True, neg_control=None, pos_control=None, threshold=None):
    """
    Function that picked up functions for normalize replica raw data
    """
    assert isinstance(replica, TCA.Replica)
    if log2_transf:
        replica = __log2_transformation(replica, channel)
    if method == 'Zscore':
        replica = __zscore_(replica, channel)
    if method == 'RobustZscore':
        replica = __robustzscore(replica, channel)
    if method == 'PercentOfSample':
        replica = __percentofsample(replica, channel)
    if method == 'RobustPercentOfSample':
        replica = __robustpercentofsample(replica, channel)
    if method == 'PercentOfControl':
        replica = __percentofcontrol(replica, channel, neg_control, pos_control)
    if method == 'RobustPercentOfControl':
        replica = __robustpercentofcontrol(replica, channel, neg_control, pos_control)
    if method == 'NormalizedPercentInhibition':
        replica = __normalizedpercentinhibition(replica, channel, neg_control, pos_control)
    if method == 'BackgroundSubstraction':
        replica = __backgroundsubstraction(replica, channel, threshold)
        # Set to zero value below zero
        replica.df.loc[replica[channel] < 0, channel] = 0
    return replica


def __log2_transformation(replica, channel):
    """
    Apply log2 transformation on replica
    :param replica: replica object
    :param channel: channel to apply
    :return: transformed replica rawdata
    """
    log.debug('Perform Log2 transformation')
    replica.df.loc[:] = replica.df[replica.df[channel] > 0]
    replica.df.loc[:, channel] = np.log2(replica.df[channel])
    return replica


def __zscore_(replica, channel):
    """
    Apply Zscore normalization on replica
    :param replica: replica object
    :param channel: channel to apply
    :return: transformed replica rawdata
    """
    log.debug('Perform Zscore')
    replica.df.loc[:, channel] = (replica.df.loc[:, channel] - np.mean(replica.df[channel])) / np.std(replica.df[channel])
    return replica


def __robustzscore(replica, channel):
    """
    Apply robust Zscore normalization on replica
    :param replica: replica object
    :param channel: channel to apply
    :return: transformed replica rawdata
    """
    log.debug('Perform robustZscore')
    replica.df.loc[:, channel] = (replica.df.loc[:, channel] - np.median(replica.df[channel])) / mad(replica.df[channel])
    return replica


def __percentofsample(replica, channel):
    """
    Apply percent of sample normalization on replica
    :param replica: replica object
    :param channel: channel to apply
    :return: transformed replica rawdata
    """
    log.debug('Perform PercentofSample')
    replica.df.loc[:, channel] = (replica.df.loc[:, channel] / np.mean(replica.df[channel])) * 100
    return replica


def __robustpercentofsample(replica, channel):
    """
    Apply robust percent of sample normalization on replica
    :param replica: replica object
    :param channel: channel to apply
    :return: transformed replica rawdata
    """
    log.debug('Perform robustPercentofSample')
    replica.df.loc[:, channel] = (replica.df.loc[:, channel] / np.median(replica.df[channel])) * 100
    return replica


def __percentofcontrol(replica, channel, neg=None, pos=None):
    """
    Apply a percent of control (ration) normalization on replica
    :param replica: replica object
    :param channel: on which channel to work
    :param neg: neg reference
    :param pos: pos reference if neg is not provided
    :return: return raw data
    """
    log.debug('Perform PercentofControl')
    if neg is None:
        if pos is None:
            raise AttributeError("Need Negative or Positive control")
        else:
            # Using positive control
            ctrl = replica.get_rawdata(channel=channel, well=pos)
    else:
        # Using negative control
        ctrl = replica.get_rawdata(channel=channel, well=neg)

    replica.df.loc[:, channel] = (replica.df.loc[:, channel] / np.mean(ctrl)) * 100
    return replica


def __robustpercentofcontrol(replica, channel, neg=None, pos=None):
    """
    Apply a percent of control (ration) normalization on replica
    :param replica: replica object
    :param channel: on which channel to work
    :param neg: neg reference
    :param pos: pos reference if neg is not provided
    :return: return raw data
    """
    log.debug('Perform PercentofControl')
    if neg is None:
        if pos is None:
            raise AttributeError("Need Negative or Positive control")
        else:
            # Using positive control
            ctrl = replica.get_rawdata(channel=channel, well=pos)
    else:
        # Using negative control
        ctrl = replica.get_rawdata(channel=channel, well=neg)

    replica.df.loc[:, channel] = (replica.df.loc[:, channel] / np.median(ctrl)) * 100
    return replica


def __normalizedpercentinhibition(replica, channel, neg=None, pos=None):
    """
    Apply a normalized percent inhibition normalization on replica
    :param replica: replica object
    :param channel: on which channel to work
    :param neg: neg reference
    :param pos: pos reference
    :return: return normalized raw data
    """
    log.debug('Perform NormalizedPercentInhibition')
    if neg is None:
        if pos is None:
            raise AttributeError("Need Negative and Positive control")
        raise AttributeError("Need Negative Control")
    neg_data = replica.get_rawdata(channel=channel, well=pos)
    pos_data = replica.get_rawdata(channel=channel, well=neg)
    replica.df.loc[:, channel] = ((np.mean(pos_data) - replica.df[channel]) / (np.mean(pos_data) - np.mean(neg_data))) * 100
    return replica


def __backgroundsubstraction(replica, channel, threshold):
    """
    Apply a background substraction by removing median of well on each wells
    :param replica: replica object
    :param channel: which channel to apply
    :return: return normalized raw data
    """
    for well in replica.get_unique_well():
        well_data = replica.get_rawdata(channel=channel, well=well)
        if threshold is not None:
            background = np.percentile(well_data, threshold)
        else:
            background = np.median(well_data)
        log.debug('{0}  Median substracted : {1}'.format(well, background))
        replica.df.loc[replica.df[replica.WellKey] == str(well), channel] = well_data - background
    return replica
