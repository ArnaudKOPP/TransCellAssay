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
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
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
        for key, value in plate.replica.items():
            min_lst.append(np.min(value.rawdata.df[channel].values))
            max_lst.append(np.max(value.rawdata.df[channel].values))

        # apply channel scaling across all replica
        for key, value in plate.replica.items():
            value.rawdata = __df_scaling(value.rawdata, min_lst, max_lst, channel, mean_scaling)
            value.isNormalized = True

        plate.isNormalized = True
    except Exception as e:
        print(e)


def __df_scaling(rawdata, min_val, max_val, channel, mean=False):
    """
    Apply feature scalling on rawdata
    :param rawdata: rawdata object
    :param min_val: min val for inf limit
    :param max_val: max val for sup limit
    :param channel: which channel to work
    :param mean: bool
    :return: normalized raw data
    """
    rawdata.df.loc[:, channel] = (rawdata.df.loc[:, channel] - min(min_val)) / (max(max_val) - min(min_val))
    if mean:
        rawdata.df.loc[:, channel] *= (sum(max_val) / len(max_val))
    return rawdata


def rawdata_variability_normalization(obj, channel, method=None, log2_transf=True, neg_control=None, pos_control=None,
                                      threshold=None):
    """
    Take a dataframe from replica object and apply desired strategy of variability normalization
    :param obj: pd.dataframe to normalize
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
                          'NormalizedPercentInhibition', 'BackgroundSubstraction', None]

        if method not in __valid_method:
            raise ValueError("Method don't exist, choose : {}".format(__valid_method))

        # check if channel is list
        if isinstance(channel, list):
            raise NotImplementedError("Multiple channels normalization don't implemented, use class functions")

        if isinstance(obj, TCA.Plate):
            for key, value in obj.replica.items():
                value.rawdata.df = __rd_norm(value.rawdata.df, channel, method, log2_transf, neg_control, pos_control,
                                             threshold)
            log.info('Raw Data normalization processing for plate {} on channel {}'.format(obj.name, channel))
        elif isinstance(obj, TCA.Replica):
            obj.rawdata.df = __rd_norm(obj.rawdata.df, channel, method, log2_transf, neg_control, pos_control,
                                       threshold)
            log.info('Raw Data normalization processing for replica {} on channel {}'.format(obj.name, channel))
        elif isinstance(obj, TCA.RawData):
            obj = __rd_norm(obj, channel, method, log2_transf, neg_control, pos_control, threshold)
            return obj
        else:
            raise TypeError("Don't take this object, only plate, replica or raw data")
    except Exception as e:
        print(e)


def __rd_norm(rawdata, channel, method=None, log2_transf=True, neg_control=None, pos_control=None, threshold=None):
    """
    Function that picked up functions for normalize raw data
    """
    if log2_transf:
        rawdata = __log2_transformation(rawdata, channel)
    if method == 'Zscore':
        rawdata = __zscore_(rawdata, channel)
    if method == 'RobustZscore':
        rawdata = __robustzscore(rawdata, channel)
    if method == 'PercentOfSample':
        rawdata = __percentofsample(rawdata, channel)
    if method == 'RobustPercentOfSample':
        rawdata = __robustpercentofsample(rawdata, channel)
    if method == 'PercentOfControl':
        rawdata = __percentofcontrol(rawdata, channel, neg_control, pos_control)
    if method == 'NormalizedPercentInhibition':
        rawdata = __normalizedpercentinhibition(rawdata, channel, neg_control, pos_control)
    if method == 'BackgroundSubstraction':
        rawdata = __backgroundsubstraction(rawdata, channel, threshold)
        rawdata.df.loc[rawdata.df[channel] < 0, channel] = 0
    return rawdata


def __log2_transformation(rawdata, channel):
    """
    Apply log2 transformation on rawdata
    :param rawdata: rawdata object
    :param channel: channel to apply
    :return: transformed rawdata
    """
    log.debug('Perform Log2 transformation')
    rawdata.df.loc[:] = rawdata.df[rawdata.df[channel] > 0]
    rawdata.df.loc[:, channel] = np.log2(rawdata.df[channel])
    return rawdata


def __zscore_(rawdata, channel):
    """
    Apply Zscore normalization on rawdata
    :param rawdata: rawdata object
    :param channel: channel to apply
    :return: transformed rawdata
    """
    log.debug('Perform Zscore')
    rawdata.df.loc[:, channel] = (rawdata.df.loc[:, channel] - np.mean(rawdata.df[channel])) / np.std(rawdata.df[channel])
    return rawdata


def __robustzscore(rawdata, channel):
    """
    Apply robust Zscore normalization on rawdata
    :param rawdata: rawdata object
    :param channel: channel to apply
    :return: transformed rawdata
    """
    log.debug('Perform robustZscore')
    rawdata.df.loc[:, channel] = (rawdata.df.loc[:, channel] - np.median(rawdata.df[channel])) / mad(rawdata.df[channel])
    return rawdata


def __percentofsample(rawdata, channel):
    """
    Apply percent of sample normalization on rawdata
    :param rawdata: rawdata object
    :param channel: channel to apply
    :return: transformed rawdata
    """
    log.debug('Perform PercentofSample')
    rawdata.df.loc[:, channel] = (rawdata.df.loc[:, channel] / np.mean(rawdata.df[channel])) * 100
    return rawdata


def __robustpercentofsample(rawdata, channel):
    """
    Apply robust percent of sample normalization on rawdata
    :param rawdata: rawdata object
    :param channel: channel to apply
    :return: transformed rawdata
    """
    log.debug('Perform robustPercentofSample')
    rawdata.df.loc[:, channel] = (rawdata.df.loc[:, channel] / np.median(rawdata.df[channel])) * 100
    return rawdata


def __percentofcontrol(rawdata, channel, neg=None, pos=None):
    """
    Apply a percent of control (ration) normalization on rawdata
    :param rawdata: rawdata object
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
            pos_data = __get_data_by_wells(rawdata, channel=channel, wells=neg)
            rawdata.df.loc[:, channel] = (rawdata.df.loc[:, channel] / np.mean(pos_data)) * 100
    else:
        # Using negative control
        neg_data = __get_data_by_wells(rawdata, channel=channel, wells=neg)
        rawdata.df.loc[:, channel] = (rawdata.df.loc[:, channel] / np.mean(neg_data)) * 100
    return rawdata


def __normalizedpercentinhibition(rawdata, channel, neg=None, pos=None):
    """
    Apply a normalized percent inhibition normalization on rawdata
    :param rawdata: rawdata object
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
    neg_data = __get_data_by_wells(rawdata, channel=channel, wells=neg)
    pos_data = __get_data_by_wells(rawdata, channel=channel, wells=pos)
    rawdata.df.loc[:, channel] = ((np.mean(pos_data) - rawdata.df[channel]) / (np.mean(pos_data) - np.mean(neg_data))) * 100
    return rawdata


def __backgroundsubstraction(rawdata, channel, threshold):
    """
    Apply a background substraction by removing median of well on each wells
    :param rawdata: rawdata object
    :param channel: which channel to apply
    :return: return normalized raw data
    """
    for well in rawdata.get_unique_well():
        well_data = rawdata.get_groupby_data().get_group(well)[channel]
        if threshold is not None:
            background = np.percentile(well_data, threshold)
        else:
            background = np.median(well_data)
        log.debug('{0}  Median substracted : {1}'.format(well, background))
        rawdata.df.loc[rawdata.df['Well'] == str(well), channel] = well_data - background
    return rawdata


def __get_data_by_wells(rawdata, channel, wells):
    """
    get all data for specified wellS
    :param wells: list of wells
    :return: return dataframe with data specified wells
    """
    datagp = rawdata.get_groupby_data()
    data = pd.DataFrame()
    for i in wells:
        if data.empty:
            data = datagp.get_group(i)[channel]
        data = data.append(datagp.get_group(i)[channel])
    return data
