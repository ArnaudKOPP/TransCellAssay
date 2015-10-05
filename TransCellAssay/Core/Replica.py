# coding=utf-8
"""
Replica implement the notion of technical replica for plate, in real, it represent one plate
"""

import os
import numpy as np
import TransCellAssay as TCA
from TransCellAssay.Core.MasterPlate import MasterPlate
import logging
log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


class Replica(MasterPlate):
    """
    Class for manipulating replica of plate, get all attribute and method from MasterPlate
    self.rawdata = rawdata              # rawdata object
    """

    def __init__(self, name, fpath, singleCells=True, skip=(), datatype='mean'):
        """
        Constructor
        :param name: name of replica
        :param fpath: Data for replica object
        :param singleCells: Are data single cell type or not
        :param skip: Well to skip
        :param datatype: Median or Mean data
        """
        super(Replica, self).__init__(name=name, datatype=datatype, skip=skip)
        log.debug('Replica created : {}'.format(name))
        self.rawdata = None
        if not singleCells:
            self.set_data(fpath)
        else:
            self.set_rawdata(fpath)

    def set_rawdata(self, input_file):
        """
        Set data in replica
        :param input_file: csv file
        """
        self.rawdata = TCA.RawData(input_file)

    def get_channels_list(self):
        """
        Get all channels/component in list
        :return: list of channel/component
        """
        return self.rawdata.get_channel_list()

    def get_valid_well(self, to_check):
        """
        :type to_check: list to check if all well are not to skip
        """
        if len(self.skip_well) < 1:
            return to_check
        if len(to_check) > 0:
            # type check
            elem = to_check[0]
            if isinstance(elem, tuple):
                tmp = [x for x in to_check if x not in self.skip_well]
                return tmp
            if isinstance(elem, str):
                tmp = [x for x in to_check if TCA.get_opposite_well_format(x) not in self.skip_well]
                return tmp
        else:
            raise ValueError('Empty List')

    def get_rawdata(self, channel=None, well=None, well_idx=False):
        """
        Get Raw data with specified param
        :param channel: defined or not channel
        :param well: defined or not which well you want, in list [] or simple string format
        :param well_idx: add or not well id
        :return: raw data in pandas dataframe
        """
        return self.rawdata.get_raw_data(channel=channel, well=well, well_idx=well_idx)

    def compute_data_channel(self, channel, datatype='mean'):
        """
        Compute data in matrix form, get mean or median for well and save them in replica object
        :param channel: which channel to keep in matrix
        :return:
        """
        if self.array is not None:
            if self._array_channel is not channel:
                log.warning('Overwriting previous channel data from {} to {}'.format(
                    self._array_channel, channel))
        self.array = self.rawdata.get_data_channel(channel=channel, type_mean=datatype)
        self.datatype = datatype
        self._array_channel = channel

    def get_data_channels(self, by='Median'):
        """
        Compute for all
        :param by : Median or Mean
        :return:
        """
        tmp = self.rawdata.get_groupby_data()
        if by == 'Median':
            return tmp.median().reset_index()
        else:
            return tmp.mean().reset_index()

    def get_data_channel(self, channel, sec=False):
        """
        Return data in matrix form, get mean or median for well
        :param channel: which channel to keep in matrix
        :param sec: want Systematic Error Corrected data ? default=False
        :return: compute data in matrix form
        """
        if sec:
            if self.array_c is None:
                raise ValueError('Process Systematic Error Correction method before')
            else:
                return self.array_c
        if self.array is None:
            self.compute_data_channel(channel)
        if channel is self._array_channel:
            return self.array
        else:
            self.compute_data_channel(channel)
            return self.array

    def get_count(self, well_key='Well'):
        """
        Get the count for all well
        :return:
        """
        gb_data = self.rawdata.get_groupby_data()
        cnt = gb_data[well_key].count().to_frame()
        cnt.columns = ['Count_'+str(self.name)]
        cnt = cnt.fillna(0)
        return cnt

    def __normalization(self, channel, method='Zscore', log_t=True, neg=None, pos=None, skipping_wells=False,
                        threshold=None):
        """
        Performed normalization on data
        :param channel; which channel to normalize
        :param method: Performed X Transformation
        :param log_t:  Performed log2 Transformation
        :param pos: positive control
        :param neg: negative control
        :param skipping_wells: skip defined wells, use it with poc and npi
        :param threshold: used in background subtraction (median is 50) you can set as you want
        """
        if not self.isNormalized:
            log.debug('Raw Data normalization processing for replica {} on channel {}'.format(self.name, channel))
            if skipping_wells:
                negative = [x for x in neg if (TCA.get_opposite_well_format(x) not in self.skip_well)]
                positive = [x for x in pos if (TCA.get_opposite_well_format(x) not in self.skip_well)]
            else:
                negative = neg
                positive = pos

            self.rawdata = TCA.rawdata_variability_normalization(self.rawdata, channel=channel,
                                                                 method=method,
                                                                 log2_transf=log_t,
                                                                 neg_control=negative,
                                                                 pos_control=positive,
                                                                 threshold=threshold)
            self.isNormalized = True
            self.compute_data_channel(channel)
        else:
            log.warning("Data are already normalized, do nothing")

    def normalization_channels(self, channels, method='Zscore', log_t=True, neg=None, pos=None, skipping_wells=False,
                               threshold=None):
        """
        Apply a normalization method to multiple
        :param pos: positive control
        :param neg: negative control
        :param channels: channel to normalize
        :param method: which method to perform
        :param log_t:  Performed log2 Transformation
        :param skipping_wells: skip defined wells, use it with poc and npi
        :param threshold: used in background subtraction (median is 50) you can set as you want
        """
        if isinstance(channels, str):
            self.__normalization(channel=channels, method=method, log_t=log_t, neg=neg, pos=pos,
                                 skipping_wells=skipping_wells, threshold=threshold)
        elif isinstance(channels, list):
            for chan in channels:
                self.__normalization(channel=chan, method=method, log_t=log_t, neg=neg, pos=pos,
                                     skipping_wells=skipping_wells, threshold=threshold)
                self.isNormalized = True
            log.warning("Choose your channels that you want to work with plate.agg_data_from_replica_channel or "
                        "replica.data_for_channel")

    def write_rawdata(self, path, name=None):
        """
        Save normalized Raw data
        :param name: Give name to file
        :param path: Where to write .csv file
        """
        if name is None:
            name = self.name
        self.rawdata.write_rawdata(path=path, name=name)


    def write_data(self, path, channel, sec=False):
        """
        Write array
        :param path:
        :param channel:
        :param sec:
        :return:
        """
        self.compute_data_channel(channel=channel)
        if sec:
            np.savetxt(fname=os.path.join(path, str(self.name)+'_'+str(channel)) + ".csv",
                           X=self.array_c, delimiter=",", fmt='%1.4f')
        else:
            np.savetxt(fname=os.path.join(path, str(self.name)+'_'+str(channel)) + ".csv",
                           X=self.array, delimiter=",", fmt='%1.4f')


    def get_file_location(self):
        """
        get all file location for all replica
        :return:
        """
        return self.rawdata.get_file_location()

    def clear_memory(self, only_cache=True):
        """
        Save memory by deleting Raw Data that use a lot of memory
        :param only_cache: Remove only cache or all
        """
        self.rawdata.clear_memory(only_caching=only_cache)
        log.debug('Saving memory')

    def __repr__(self):
        """
        Definition for the representation
        """
        return ("\nReplica ID : " + repr(self.name) +
                repr(self.rawdata) +
                "\nData normalized : " + repr(self.isNormalized) +
                "\nData systematic error removed : " + repr(self.isSpatialNormalized) + "\n")

    def __str__(self):
        """
        Definition for the print
        """
        return self.__repr__()
