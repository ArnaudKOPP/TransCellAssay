# coding=utf-8
"""
Replica implement the notion of technical replica for plate, in real, it represent one plate
"""

import os
import numpy as np
import TransCellAssay as TCA
import logging
log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


class Replica(object):
    """
    Class for manipulating replica of plate

    self.name = ""                      # Name of replica
    self.rawdata = rawdata              # rawdata object
    self.isNormalized = False           # are the data normalized
    self.isSpatialNormalized = False    # systematics error removed or not
    self.datatype = "median"            # median or mean of data
    self.array = None                   # matrix that contain mean/median of interested channels to analyze
    self._array_channel = None          # which channel is stored in data
    self.array_c = None                 # matrix that contain spatial data corrected
    self.skip_well = ()                 # list of well to skip in control computation, stored in this form ((1, 1), (5, 16))
    self._is_cutted = False             # Bool for know if plate are cutted
    self._rb = None                     # row begin of cutting operation
    self._re = None                     # row end of cutting operation
    self._cb = None                     # col begin of cutting operation
    self._ce = None                     # col end of cutting operation
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
        log.debug('Replica created : {}'.format(name))
        self.name = name
        self.rawdata = None
        self.isNormalized = False
        self.isSpatialNormalized = False
        self.datatype = datatype
        self._array_channel = None
        self.array = None
        self.array_c = None
        if not singleCells:
            self.set_array_data(fpath)
        else:
            self.set_rawdata(fpath)
        self.skip_well = skip
        self._is_cutted = False
        self._rb = None
        self._re = None
        self._cb = None
        self._ce = None

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

    def set_array_data(self, array, array_type='median'):
        """
        Set attribute data matrix into self.array
        This method is designed for 1Data/Well or for manual analysis
        :param array: numpy array with good shape like platemap
        :param array_type: median or mean data
        """
        __valid_datatype = ['median', 'mean']
        if isinstance(array, np.ndarray):
            if array_type not in __valid_datatype:
                raise ValueError("Must provided data type, possibilities : {}".format(__valid_datatype))
            log.info("Import of none single cell data")
            self.array = array
            self.datatype = array_type
        else:
            raise AttributeError("Must provided numpy ndarray")

    def set_name(self, info):
        """
        set name for the replica
        :param info: info on replica
        :return:
        """
        self.name = info

    def get_name(self):
        """
        return name from replica
        :return: info
        """
        return self.name

    def set_skip_well(self, to_skip):
        """
        Set the well to skip in neg or pos control
        :param to_skip: list of well to skip (1,3) or B3
        """
        well_list = list()
        for elem in to_skip:
            if isinstance(elem, tuple):
                well_list.append(elem)
            elif isinstance(elem, str):
                well_list.append(TCA.get_opposite_well_format(elem))
            else:
                pass
        self.skip_well = well_list

    def get_skip_well(self):
        """
        Get the skipped Well
        """
        return self.skip_well

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

    def cut(self, rb, re, cb, ce):
        """
        Cut the replica to 'zoom' into a defined zone, for avoiding crappy effect during SEC process
        :param rb: row begin
        :param re: row end
        :param cb: col begin
        :param ce: col end
        """
        if self._is_cutted:
            raise AttributeError('Already cutted')
        log.debug('Cutting operation on replica : {0} (param {1}:{2},{3}:{4})'.format(self.name, rb, re, cb, ce))
        if self.array is not None:
            self.array = self.array[rb: re, cb: ce]
        if self.array_c is not None:
            self.array_c = self.array_c[rb: re, cb: ce]
        self._is_cutted = True
        self._rb = rb
        self._re = re
        self._cb = cb
        self._ce = ce

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

    def systematic_error_correction(self, algorithm='Bscore', method='median', verbose=False, save=True,
                                    max_iterations=100, alpha=0.05, epsilon=0.01, skip_col=[], skip_row=[],
                                    trimmed=0.0):
        """
        Apply a spatial normalization for remove edge effect
        The Bscore method showed a more stable behavior than MEA and PMP only when the number of rows and columns
        affected by the systematics error, hit percentage and systematic error variance were high (mainly du to a
        mediocre performance of the t-test in this case). MEA was generally the best method for correcting
        systematic error within 96-well plates, whereas PMP performed better for 384 /1526 well plates.

        :param alpha: alpha for some algorithm
        :param algorithm: Bscore, MEA, PMP or diffusion model technics, default = Bscore
        :param method: median or mean data
        :param verbose: Output in console
        :param save: save the result into self.SECData, default = False
        :param max_iterations: maximum iterations loop, default = 100
        :param epsilon: epsilon parameters for PMP
        :param skip_col: index of col to skip in MEA or PMP
        :param skip_row: index of row to skip in MEA or PMP
        :param trimmed: Bscore only for average method only, trimmed the data with specified value, default is 0.0
        """
        global corrected_data_array
        __valid_sec_algo = ['Bscore', 'BZscore', 'PMP', 'MEA', 'DiffusionModel']

        if algorithm not in __valid_sec_algo:
            log.error('Algorithm is not good choose : {}'.format(__valid_sec_algo))
            raise ValueError()

        if self.array is None:
            log.error("Use first : compute_data_for_channel")
            raise AttributeError()

        else:
            if self.isSpatialNormalized:
                log.warning('SEC already performed -> overwriting previous sec data')

            log.debug('Systematic Error Correction processing : {} -> replica {}'.format(algorithm, self.name))

            if algorithm == 'Bscore':
                ge, ce, re, corrected_data_array, tbl_org = TCA.median_polish(self.array.copy(), method=method,
                                                                              max_iterations=max_iterations,
                                                                              trimmed=trimmed,
                                                                              verbose=verbose)

            if algorithm == 'BZscore':
                ge, ce, re, corrected_data_array, tbl_org = TCA.bz_median_polish(self.array.copy(), method=method,
                                                                                 max_iterations=max_iterations,
                                                                                 trimmed=trimmed,
                                                                                 verbose=verbose)

            if algorithm == 'PMP':
                corrected_data_array = TCA.partial_mean_polish(self.array.copy(), max_iteration=max_iterations,
                                                               verbose=verbose, alpha=alpha, epsilon=epsilon,
                                                               skip_col=skip_col, skip_row=skip_row)

            if algorithm == 'MEA':
                corrected_data_array = TCA.matrix_error_amendmend(self.array.copy(), verbose=verbose, alpha=alpha,
                                                                  skip_col=skip_col, skip_row=skip_row)

            if algorithm == 'DiffusionModel':
                corrected_data_array = TCA.diffusion_model(self.array.copy(), max_iterations=max_iterations,
                                                           verbose=verbose)
            if save:
                self.array_c = corrected_data_array
                self.isSpatialNormalized = True

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
