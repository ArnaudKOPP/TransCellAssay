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
    :return: return result into dict of dataframe, key are channel and value a df with results
    """
    if not isinstance(channels, list):
        channels = list(channels)
    res = collections.OrderedDict()
    for chan in channels:
        log.info('Plate analysis for channel {}'.format(chan))
        res[chan] = plate_channel_analysis(plate=plate, channel=chan, neg=neg, pos=pos, threshold=threshold,
                                           percent=percent, fixed_threshold=fixed_threshold, path=path, tag=tag,
                                           clean=clean)
    return res

def plate_channel_analysis(plate, channel=None, neg=None, pos=None, threshold=50, percent=True, fixed_threshold=False,
                           path=None, tag="", clean=False):
    assert isinstance(plate, TCA.Plate)

    if not len(plate) > 0:
        log.error('Empty Plate Object, add some replica to perform PlateAnalysis')
        return

    if threshold >= 100 and percent:
        log.warning('Threshold cannot be > 100 with percent')
        percent = False
        fixed_threshold = True

    if plate._is_cutted:
        log.error('Plate was cutted, for avoiding undesired effect, plate analysis cannot be performed')
        raise NotImplementedError()
    log.info('Perform plate analysis for {0} on channel {1}'.format(plate.name, channel))


    if channel is not None:
        plate.agg_data_from_replica_channel(channel=channel, use_sec_data=False, forced_update=True)

    platemap = plate.get_platemap()
    size = platemap.shape()
    WellKey = 'Well'
    __SIZE__ = (size[0] * size[1])
    ResultatsArray = Result(size=__SIZE__)
    x = platemap.as_dict()

    ## Init results dataframe
    ResultatsArray.init_gene_well(x)
    ResultatsArray.values['PlateName'] = np.repeat([plate.name], __SIZE__)

    if neg is not None:
        if not isinstance(neg, list):
            neg_well = plate.platemap.search_well(neg)
        else:
            neg_well = neg
    else:
        log.info('No Negative control provided, only work with fixed_treshold to True')

    CellsCountReplicas = collections.OrderedDict()
    MeanWellsReplicas = collections.OrderedDict()
    MedianWellsReplicas = collections.OrderedDict()
    PercentCellsReplicas = collections.OrderedDict()
    PercentCellsSDReplicas = collections.OrderedDict()

    # ########## iterate over replica
    i = 1
    for k, replica in plate.replica.items():
        log.debug("Iteration on replica : {0} | {1} | {2}".format(replica.name, __SIZE__, len(replica.rawdata.df)))
        # ########## cell count
        datagb = replica.rawdata.get_groupby_data()
        cellcount = datagb[WellKey].count().to_dict()
        log.debug("     Determine Cells count")
        CellsCount = collections.OrderedDict()
        for key, value in cellcount.items():
            try:
                CellsCountReplicas.setdefault(key, []).append(value)
                CellsCount[key] = value
            except KeyError:
                pass
        ResultatsArray.add_data(CellsCount, 'CellsCount_' + str(replica.name))

        if channel is not None:
            # ########## positive Cell
            # # threshold value for control
            if fixed_threshold:
                ThresholdValue = threshold
                log.info('     Fixed Threshold value used: {}'.format(ThresholdValue))
            else:
                if percent:
                    ControlData = replica.get_rawdata(channel=channel, well=neg_well)
                    ThresholdValue = np.percentile(ControlData, threshold)
                    log.info('     Percent {0} Threshold value used: {1}'.format(threshold, ThresholdValue))
                else:
                    ControlData = replica.get_rawdata(channel=channel, well=neg_well)
                    ThresholdValue = np.mean(ControlData)
                    log.info('     Neg Mean Threshold value used: {}'.format(ThresholdValue))

            # ########## variability
            well_list = replica.rawdata.get_unique_well()
            # iterate on well
            PercentCells = collections.OrderedDict()
            log.debug("     Determine Positive Cells percentage")
            for well in well_list:
                xdata = datagb.get_group(well)[channel]
                MeanWellsReplicas.setdefault(well, []).append(np.mean(xdata.values))
                MedianWellsReplicas.setdefault(well, []).append(np.median(xdata.values))
                len_total = len(xdata.values)
                len_thres = len(np.extract(xdata.values > ThresholdValue, xdata.values))
                # # include in dict key is the position and value is a %
                PercentCellsReplicas.setdefault(well, []).append(((len_thres / len_total) * 100))
                PercentCells[well] = (len_thres / len_total) * 100
            ResultatsArray.add_data(PercentCells, 'PosCells_' + str(replica.name))
            ResultatsArray.values[replica.name+'_'+replica.datatype+'_value'] = replica.array.flatten().reshape(__SIZE__, 1)
            i += 1

    if channel is not None:
        # ########## p-value and fdr for percent cell
        if neg is not None:
            if len(plate) > 1:
                log.debug("Perform T-Test on positive Cells percentage")
                NegData = list()
                for x in neg_well:
                    NegData.extend(PercentCellsReplicas[x])
                ## or this but don't work when data are missing ????
                # neg_data = [PercentCellsReplicas[x] for x in neg_well]
                NegData = np.array(NegData).flatten()
                pvalue = collections.OrderedDict()
                for key, value in PercentCellsReplicas.items():
                    x = stats.ttest_ind(value, NegData, equal_var=False)
                    pvalue[key] = x[1]

                ResultatsArray.add_data(pvalue, 'TTest p-value')
                ResultatsArray.values["TTest fdr"] = TCA.adjustpvalues(pvalues=ResultatsArray.values["TTest p-value"])

        # ########## variability
        if len(plate) > 1:
            log.debug("Variability determination")
            MeanSD = dict([(i, np.std(v)) for i, v in MeanWellsReplicas.items()])
            MedianSD = dict([(i, np.std(v)) for i, v in MedianWellsReplicas.items()])
            ResultatsArray.add_data(MeanSD, 'Mean std')
            ResultatsArray.add_data(MedianSD, 'Median std')

        MeanWellsReplicas = dict([(i, sum(v) / len(v)) for i, v in MeanWellsReplicas.items()])
        MedianWellsReplicas = dict([(i, sum(v) / len(v)) for i, v in MedianWellsReplicas.items()])
        ResultatsArray.add_data(MeanWellsReplicas, 'Mean')
        ResultatsArray.add_data(MedianWellsReplicas, 'Median')

        # ########## positive cell
        # determine the mean of replicat
        MeanPercentCells = dict([(i, sum(v) / len(v)) for i, v in PercentCellsReplicas.items()])
        ResultatsArray.add_data(MeanPercentCells, 'PositiveCells')

        # ########## determine the standart deviation of % Cells
        if len(plate) > 1:
            for key, value in PercentCellsReplicas.items():
                PercentCellsSDReplicas[key] = np.std(value)

            ResultatsArray.add_data(PercentCellsSDReplicas, 'PositiveCells std')


    # ########## Cell count and std
    if len(plate) > 1:
        MeanCellsCountSD = {}
        for key, value in CellsCountReplicas.items():
            MeanCellsCountSD[key] = np.std(value)
        ResultatsArray.add_data(MeanCellsCountSD, 'CellsCount std')

    MeanCellsCount = dict([(i, sum(v) / len(v)) for i, v in CellsCountReplicas.items()])
    ResultatsArray.add_data(MeanCellsCount, 'CellsCount')

    # ########## toxicity index
    if neg is not None:
        log.debug("Toxicity determination")
        # ### 0 idx is the max cell of all plate
        # max_cell = max(MeanCellsCount.values())
        # ### 0 idx is the neg control
        temp = list()
        for neg in neg_well:
            temp.extend(CellsCountReplicas[neg])
        max_cell = np.mean(temp)
        ## or this but don't work when data are missing ????
        # max_cell = np.mean([CellsCountReplicas[neg] for neg in neg_well])
        min_cell = min(MeanCellsCount.values())
        ToxIdx = {}
        for key, item in MeanCellsCount.items():
            ToxIdx[key] = (max_cell - item) / (max_cell - min_cell)

        ResultatsArray.add_data(ToxIdx, 'Toxicity')

    # ########## viability index
    if neg is not None:
        if pos is not None:
            log.debug("Viability determination")
            pos_well = plate.platemap.search_well(pos)
            neg_val = [MeanCellsCount[x] for x in neg_well]
            pos_val = [MeanCellsCount[x] for x in pos_well]
            Viability = {}
            for key, item in MeanCellsCount.items():
                Viability[key] = (item - np.mean(pos_val) - 3 * np.std(pos_val)) / np.abs(
                    np.mean(neg_val) - np.mean(pos_val))

            ResultatsArray.add_data(Viability, 'Viability')
        else:
            log.info('No positive control provided, no viability performed')


    ### Remove row with cellscount is 0
    if clean:
        ResultatsArray.values = ResultatsArray.values[ResultatsArray.values['CellsCount'] > 0]

    if path is not None:
        try:
            if channel is not None:
                filepath = os.path.join(path, 'PlateAnalyzis_' + str(plate.name) + '_' + str(channel) + "_" + str(tag)
                                        + '.csv')
                ResultatsArray.write(file_path=filepath)
            else:
                filepath = os.path.join(path, 'PlateAnalyzis_' + str(plate.name) + "_" + str(tag) + '.csv')
                ResultatsArray.write(file_path=filepath)
        except Exception as e:
            log.error('Error during writing data from PlateAnalyzis : {}'.format(e))

    if channel is not None:
        return ResultatsArray, ThresholdValue
    else:
        ResultatsArray.values.drop(['PositiveCells', 'Mean', 'Median'], axis=1, inplace=True)
        return ResultatsArray


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
