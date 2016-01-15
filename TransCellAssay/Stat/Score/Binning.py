# coding=utf-8
"""
Function for making binning aka intervals analysis
"""

import TransCellAssay as TCA
import numpy as np
import pandas  as pd
import logging
import collections

log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def Binning(Plate, chan, bins=None, nbins=10, percent=True):
    """
    Make binning (intervals) for various channels, return a dict with key is replica name and value the df of binning
    param Plate: Plate Object
    param chan: On which channel make the binning
    param bins: default is None, but can provided custom intervals
    param nbins: by default, make 10 bins with min and max of channel as extreme
    return a dict with key is rep name and value a dataframe with binning data
    """
    assert isinstance(Plate, TCA.Plate)
    log.info("Binning process on : {}".format(Plate.name))

    frames = collections.OrderedDict()
    for key, value in Plate:
        assert chan in value.get_channels_list(), "Given channel {0} -> not in available channels : {1}".format(chan, value.get_channels_list())
        log.debug("Iterate on : {}".format(key))

        ## Create Bins
        if bins is None:
            bins = np.linspace(np.min(value.df[chan].values), np.max(value.df[chan].values), nbins)

        x = value.df.groupby(by=["Well", pd.cut(value.df[chan], bins)]).count()[chan]
        x = x.unstack()

        if percent:
            x = x.iloc[:, :].apply(lambda a: a / x.sum(axis=1) * 100)

        frames[key] = x.fillna(0)

    return frames
