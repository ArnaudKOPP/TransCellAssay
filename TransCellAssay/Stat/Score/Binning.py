# coding=utf-8
"""
Function for making binning aka intervals analysis
"""

import TransCellAssay as TCA
import numpy as np
import pandas  as pd
import logging

log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def Binning(Plate, chan, bins=None, nbins=10):
    """
    Make binning (intervals) for various channels
    param Plate: Plate Object
    param chan: On which channel make the binning
    param bins: default is None, but can provided custom intervals
    param nbins: by default, make 10 bins with min and max of channel as extreme
    """
    assert isinstance(Plate, TCA.Plate)
    log.info("Binning process on : {}".format(Plate.name))
    DF = None

    for key, value in Plate:
        assert chan in value.get_channels_list(), "Given channel {0} -> not in available channels : {1}".format(chan, value.get_channels_list())
        log.debug("Iterate on : {}".format(key))
        ## Create Bins
        if bins is None:
            bins = np.linspace(np.min(value.df[chan].values), np.max(value.df[chan].values), nbins)

        x = value.df.groupby(by=["Well", pd.cut(value.df[chan], bins)]).count()[chan]

        x.index.names = ['Well', 'Bins']
        x.name = str(chan)+"_"+str(key)

        if DF is None:
            DF = x.reset_index()
        else:
            DF = pd.merge(DF, x.reset_index(), on=['Well', 'Bins'])

    ## Fill NaN by 0
    DF = DF.fillna(0)

    return DF
