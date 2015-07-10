# coding=utf-8
"""
Compute basics score for plate and store result into a Result object.
Compute Cells Count, percent of positive Cells, viability and toxicity per Wells.
"""

import collections
import os
import logging
import numpy as np
import pandas as pd
from scipy import stats
import TransCellAssay as TCA

log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def plate_channels_analysis(plate, channels, neg=None, pos=None, threshold=50, percent=True, fixed_threshold=False,
                            path=None, tag="", clean=False):
    """
    Like plate_channel_analysis, do a plate analysis but for multiple channels and parameters
    :param plate: plate object
    :param channels: list of channels
    :param neg: negative control
    :param pos: positive control, is optional
    :param threshold: fixe the percent of positive well found in negative control well
    :param percent: True if threshold value is percent, False if we want to give a value
    :param fixed_threshold: use given threshold (value mode) for all well
    :param path: path where file will be saved
    :param tag: add this tag at end of file name
    :param clean: if True, remove all row/Well that don't contain cells
    :return: return result into a dataframe
    """
    if not isinstance(channels, list):
        channels = list(channels)
    for chan in channels:
        log.info('Plate analysis for channel {}'.format(chan))
        plate_channel_analysis(plate=plate, channel=chan, neg=neg, pos=pos, threshold=threshold, percent=percent,
                               fixed_threshold=fixed_threshold, path=path, tag=tag, clean=clean)


def plate_channel_analysis(plate, channel, neg=None, pos=None, threshold=50, percent=True, fixed_threshold=False, path=None,
                           tag="", clean=False):
    assert isinstance(plate, TCA.Plate)
    if not len(plate) > 0:
        log.error('Empty Plate Object, add some replica to perform PlateAnalysis')
        return

    if threshold >= 100 and percent:
        log.warning('Threshold cannot be > 100 with percent')
        percent = False

    if plate._is_cutted:
        log.error('Plate was cutted, for avoiding undesired effect, plate analysis cannot be performed')
        raise NotImplementedError()
    log.info('Perform plate analysis for {0} on channel {1}'.format(plate.name, channel))

    platemap = plate.get_platemap()

    size = platemap.shape()
    WellKey = 'Well'
    __SIZE__ = (size[0] * size[1])
    result_array = Result(size=__SIZE__)
    x = platemap.as_dict()

    result_array.init_gene_well(x)
    result_array.values['PlateName'] = np.repeat([plate.name], __SIZE__)

    if neg is not None:
        neg_well = plate.platemap.search_well(neg)
    else:
        log.info('No Negative control provided, only work with fixed_treshold to True')

    cell_count_all_replica = collections.OrderedDict()
    mean_well_value_all_replica = collections.OrderedDict()
    median_well_value_all_replica = collections.OrderedDict()
    percent_cell_all_replica = collections.OrderedDict()
    percent_cell_sd = collections.OrderedDict()

    # ########## iterate over replica
    i = 1
    for k, replica in plate.replica.items():
        log.debug("Iteration on replica : {0} | {1} | {2}".format(replica.name, __SIZE__, len(replica.rawdata.df)))
        # ########## cell count
        datagb = replica.rawdata.get_groupby_data()
        cellcount = datagb[WellKey].count().to_dict()
        log.debug("     Determine Cells count")
        cell_count = collections.OrderedDict()
        for key, value in cellcount.items():
            try:
                cell_count_all_replica.setdefault(key, []).append(value)
                cell_count[key] = value
            except KeyError:
                pass
        result_array.add_data(cell_count, 'CellsCount_' + str(replica.name))

        # ########## positive Cell
        # # threshold value for control
        if fixed_threshold:
            threshold_value = threshold
            log.info('     Fixed Threshold value used: {}'.format(threshold_value))
        else:
            if percent:
                data_control = replica.get_rawdata(channel=channel, well=neg_well)
                threshold_value = np.percentile(data_control, threshold)
                log.info('     Percent {0} Threshold value used: {1}'.format(threshold, threshold_value))
            else:
                data_control = replica.get_rawdata(channel=channel, well=neg_well)
                threshold_value = np.mean(data_control)
                log.info('     Neg Mean Threshold value used: {}'.format(threshold_value))

        # ########## variability
        well_list = replica.rawdata.get_unique_well()
        # iterate on well
        percent_cell = collections.OrderedDict()
        log.debug("     Determine Positive Cells percentage")
        for well in well_list:
            xdata = datagb.get_group(well)[channel]
            mean_well_value_all_replica.setdefault(well, []).append(np.mean(xdata.values))
            median_well_value_all_replica.setdefault(well, []).append(np.median(xdata.values))
            len_total = len(xdata.values)
            len_thres = len(np.extract(xdata.values > threshold_value, xdata.values))
            # # include in dict key is the position and value is a %
            percent_cell_all_replica.setdefault(well, []).append(((len_thres / len_total) * 100))
            percent_cell[well] = (len_thres / len_total) * 100
        result_array.add_data(percent_cell, 'PosCells_' + str(replica.name))
        i += 1

    # ########## p-value and fdr for percent cell
    if neg is not None:
        if len(plate) > 1:
            log.debug("Perform T-Test on positive Cells percentage")
            neg_data = [percent_cell_all_replica[x] for x in neg_well]
            neg_data = np.array(neg_data).flatten()
            pvalue = collections.OrderedDict()
            for key, value in percent_cell_all_replica.items():
                x = stats.ttest_ind(value, neg_data, equal_var=False)
                pvalue[key] = x[1]

            result_array.add_data(pvalue, 'TTest p-value')
            result_array.values["TTest fdr"] = TCA.adjustpvalues(pvalues=result_array.values["TTest p-value"])

    # ########## Cell count and std
    if len(plate) > 1:
        sdvalue = {}
        for key, value in cell_count_all_replica.items():
            sdvalue[key] = np.std(value)
        result_array.add_data(sdvalue, 'CellsCount std')

    meancount = dict([(i, sum(v) / len(v)) for i, v in cell_count_all_replica.items()])
    result_array.add_data(meancount, 'CellsCount')

    # ########## toxicity index
    if neg is not None:
        log.debug("Toxicity determination")
        # ### 0 idx is the max cell of all plate
        # max_cell = max(meancount.values())
        # ### 0 idx is the neg control
        max_cell = np.mean([cell_count_all_replica[neg] for neg in neg_well])
        min_cell = min(meancount.values())
        txidx = {}
        for key, item in meancount.items():
            txidx[key] = (max_cell - item) / (max_cell - min_cell)

        result_array.add_data(txidx, 'Toxicity')

    # ########## viability index
    if neg is not None:
        if pos is not None:
            log.debug("Viability determination")
            pos_well = plate.platemap.search_well(pos)
            neg_val = [meancount[x] for x in neg_well]
            pos_val = [meancount[x] for x in pos_well]
            viability = {}
            for key, item in meancount.items():
                viability[key] = (item - np.mean(pos_val) - 3 * np.std(pos_val)) / np.abs(
                    np.mean(neg_val) - np.mean(pos_val))

            result_array.add_data(viability, 'Viability')
        else:
            log.info('No positive control provided, no viability performed')

    # ########## variability
    if len(plate) > 1:
        log.debug("Variability determination")
        std = dict([(i, np.std(v)) for i, v in mean_well_value_all_replica.items()])
        stdm = dict([(i, np.std(v)) for i, v in median_well_value_all_replica.items()])
        result_array.add_data(std, 'Mean std')
        result_array.add_data(stdm, 'Median std')

    mean_well_value_all_replica = dict([(i, sum(v) / len(v)) for i, v in mean_well_value_all_replica.items()])
    median_well_value_all_replica = dict([(i, sum(v) / len(v)) for i, v in median_well_value_all_replica.items()])
    result_array.add_data(mean_well_value_all_replica, 'Mean')
    result_array.add_data(median_well_value_all_replica, 'Median')

    # ########## positive cell
    # determine the mean of replicat
    dict_percent_cell = dict([(i, sum(v) / len(v)) for i, v in percent_cell_all_replica.items()])
    result_array.add_data(dict_percent_cell, 'PositiveCells')

    # ########## determine the standart deviation of % Cells
    if len(plate) > 1:
        for key, value in percent_cell_all_replica.items():
            percent_cell_sd[key] = np.std(value)

        result_array.add_data(percent_cell_sd, 'PositiveCells std')

    if clean:
        result_array.values = result_array.values[result_array.values['CellsCount'] > 0]

    if path is not None:
        try:
            filepath = os.path.join(path, 'PlateAnalyzis_' + str(plate.name) + '_' + str(channel) + "_" + str(tag)
                                    + '.csv')
            result_array.write(file_path=filepath)
        except Exception as e:
            log.error('Error during writing data from PlateAnalyzis : {}'.format(e))
    return result_array


class Result(object):
    """
    Class Result is especially created for plateAnalyzis.
    This class store data with dict in input, where key are well and item are data.
    """

    def __init__(self, size=None):
        """
        Constructor
        if size is not given, init by 386 plate size, defined size if 96 or 1526 plate well
        :return: none init only dataframe
        """
        if size is None:
            size = 96
        self.values = pd.DataFrame(np.zeros(size, dtype=[('PlateName', object), ('PlateMap', object), ('Well', object),
                                                         ('CellsCount', float), ('PositiveCells', float),
                                                         ('Mean', float), ('Median', float), ('Viability', float),
                                                         ('Toxicity', float)]))

        self._genepos_genename = {}  # # To save Well (key) and Gene position (value)

    def init_gene_well(self, gene_list):
        """
        Add gene and well into the record Array in the first/second column
        :param gene_list: Dict with key are Well and Value are geneName
        :return:
        """
        try:
            i = 0
            for k, v in gene_list.items():
                self.values.loc[i, 'PlateMap'] = v
                self.values.loc[i, 'Well'] = k
                self._genepos_genename[k] = i
                i += 1
        except Exception as e:
            print(e)

    def add_data(self, datadict, col):
        """
        Insert Value from a dict where key = GeneName/pos and Value are value to insert
        Prefer by = pos in case of empty well
        :param datadict: dict that contain value to insert with key are GeneName or Pos/Well
        :param col: columns name to insert data
        """
        try:
            if col not in self.values.columns:
                self.values[col] = 0
            for item, value in datadict.items():
                self.values.loc[self._genepos_genename[item], col] = value
        except Exception as e:
            print(e)

    def write(self, file_path, frmt='csv'):
        """
        Save Result Array into csv
        :param file_path:
        :param frmt: csv or xlsx format to save
        """
        try:
            if frmt is 'csv':
                pd.DataFrame(self.values).to_csv(file_path, index=False, header=True)
            elif frmt is 'xlsx':
                pd.DataFrame(self.values).to_excel(file_path, sheet_name='Single Cell properties result', index=False,
                                                   header=True)
            log.info('Writing : {}'.format(file_path))
        except:
            try:
                if frmt is 'csv':
                    np.savetxt(fname=file_path, X=self.values, delimiter=';')
                    log.info('Writing : {}'.format(file_path))
                else:
                    log.error("Can't save data in xlsx format")
                    raise IOError()
            except Exception as e:
                log.error('Error in saving results data :', e)
                raise IOError()

    def __repr__(self):
        """
        Definition for the representation
        :return:
        """
        try:
            return "Result of single Cell properties: \n" + repr(pd.DataFrame(self.values))
        except Exception as e:
            print(e)

    def __str__(self):
        """
        Definition for the print
        :return:
        """
        try:
            return self.__repr__()
        except Exception as e:
            print(e)
