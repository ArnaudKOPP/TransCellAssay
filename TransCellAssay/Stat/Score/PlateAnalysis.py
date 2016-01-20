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
__copyright__ = "© 2014-2016 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"

def getEventsCounts(plate):
    """
    Get the Events Count from single Cells data
    :param plate: Plate object with some replica
    :return: DataFrame with plate count
    """
    assert isinstance(plate, TCA.Plate)
    log.info("Get Events Counts on {}".format(plate.name))
    df = PlateChannelsAnalysis(plate)
    return df

def getThreshold(plate, ctrl, channels, threshold, percent=True, fixed_threshold=False):
    """
    compute threshold
    :param plate: plate object
    :param channel: list of channels
    :param ctrl: control where determine value of threshold
    :param threshold: fixe the percent of positive well found in  control well
    :param percent: True if threshold value is percent, False if we want to give a value
    :param fixed_threshold: use given threshold (value mode) for all well
    return a dict with value Chan -> repId -> value
    """
    assert isinstance(plate, TCA.Plate)
    ThresholdVALUE = {}

    if channels is not None:

        if not isinstance(channels, list):
            channels = [channels]

        ThresholdVALUE = dict([(i, dict([(repname, 0) for repname, rep in plate])) for i in channels])

        if ctrl is not None:
            ## if neg is list -> suppose that its a list of well
            if not isinstance(ctrl, list):
                neg_well = plate.platemap.search_well(ctrl)
            else:
                neg_well = ctrl
        else:
            if channels is not None:
                log.warning('No Negative control provided, work only with fixed value of threshold')
                fixed_threshold = True

        ## iterate over channels
        for chan in channels:

            for repName, replica in plate:
                datagb = replica.get_groupby_data()
                ########### POSITIVE CELLS %
                # # threshold value for control

                if isinstance(threshold, dict):
                    THRES = threshold[chan]
                else:
                    THRES = threshold

                if THRES >= 100 and percent:
                    log.warning('Threshold cannot be > 100 with percent')
                    percent = False
                    fixed_threshold = True

                if fixed_threshold:
                    ThresholdValue = THRES
                    log.debug('     Fixed Threshold value used: {}'.format(ThresholdValue))
                else:
                    if percent:
                        ControlData = replica.get_rawdata(channel=chan, well=neg_well)
                        ThresholdValue = np.percentile(ControlData, THRES)
                        log.debug('     Percent {0} Threshold value used: {1}'.format(THRES, ThresholdValue))
                    else:
                        ControlData = replica.get_rawdata(channel=chan, well=neg_well)
                        ThresholdValue = np.mean(ControlData)
                        log.debug('     Neg Mean Threshold value used: {}'.format(ThresholdValue))

                ThresholdVALUE[chan][repName] = ThresholdValue

    return ThresholdVALUE


def PlateChannelsAnalysis(plate, channels=None, neg=None, pos=None, threshold=50, percent=True, fixed_threshold=False,
                          clean=False):
    """
    Like plate_channel_analysis, do a plate analysis but for multiple channels and parameters
    :param plate: plate object
    :param channel: list of channels
    :param neg: negative control
    :param pos: positive control, is optional
    :param threshold: fixe the percent of positive well found in negative control well
    :param percent: True if threshold value is percent, False if we want to give a value
    :param fixed_threshold: use given threshold (value mode) for all well
    :param clean: if True, remove all row/Well that don't contain cells
    :return: result into dataframe
    """
    assert isinstance(plate, TCA.Plate)

    if not len(plate) > 0:
        log.error('Empty Plate Object, add some replica to perform PlateAnalysis')
        return

    if plate._is_cutted:
        log.error('Plate was cutted, for avoiding undesired effect, plate analysis cannot be performed')
        raise NotImplementedError()

    __WellKey = 'Well'

    PM = plate.get_platemap()
    SIZE = PM.shape(alt_frmt=True)
    ResultatsArray = Result(plate)

    ## CELLS COUNT STUFF
    CellsCountReplicas = {}
    for repName, replica in plate:
        log.debug("Iteration on replica : {0} | {1} cells".format(replica.name, len(replica.df)))
        cellcount = replica.get_groupby_data()[__WellKey].count().to_dict()
        CellsCount = {}
        for key, value in cellcount.items():
            try:
                CellsCountReplicas.setdefault(key, []).append(value)
                CellsCount[key] = value
            except KeyError:
                pass
        ResultatsArray.add_data(CellsCount, "Plate",'CellsCount_' + str(replica.name))
    # ########## Cell count and std
    if len(plate) > 1:
        MeanCellsCountSD = {}
        for key, value in CellsCountReplicas.items():
            MeanCellsCountSD[key] = np.std(value)
        ResultatsArray.add_data(MeanCellsCountSD, "Plate", 'CellsCount std')

    MeanCellsCount = dict([(i, sum(v) / len(v)) for i, v in CellsCountReplicas.items()])
    ResultatsArray.add_data(MeanCellsCount, "Plate",'CellsCount')

    ## ANALYSING CHANNELS
    if channels is not None:
        log.info('Perform plate analysis for {0} on channels :{1}'.format(plate.name, channels))
        if not isinstance(channels, list):
            channels = [channels]

        if neg is not None:
            ## if neg is list -> suppose that its a list of well
            if not isinstance(neg, list):
                neg_well = plate.platemap.search_well(neg)
            else:
                neg_well = neg
        else:
            if channels is not None:
                log.info('  No Negative control provided, work only with fixed value of threshold')
                fixed_threshold = True

        ThresholdVALUE = getThreshold(plate, ctrl=neg, channels=channels, threshold=threshold, percent=percent,
                        fixed_threshold=False)


        ## iterate over channels
        for chan in channels:
            ## these dict are for storing value accross all replica
            MeanWellsReplicas = {}
            MedianWellsReplicas = {}
            PercentCellsReplicas = {}
            PercentCellsSDReplicas = {}

            for repName, replica in plate:
                datagb = replica.get_groupby_data()
                ########### POSITIVE CELLS %
                # # threshold value for control
                ThresholdValue = ThresholdVALUE[chan][repName]

                ########### VARIABILITY & % OF POSITIVE CELLS
                well_list = replica.get_unique_well()
                # iterate on well
                PercentCells = {}
                MeanCells = {}
                MedianCells = {}
                SdCells = {}
                MadCells = {}
                log.debug(" Determine Positive Cells percentage")
                for well in well_list:
                    xdata = datagb.get_group(well)[chan]
                    len_total = len(xdata.values)
                    len_thres = len(np.extract(xdata.values > ThresholdValue, xdata.values))
                    # # include in dict key is the position and value is a %
                    PercentCellsReplicas.setdefault(well, []).append(((len_thres / len_total) * 100))
                    PercentCells[well] = (len_thres / len_total) * 100

                    mean = np.mean(xdata.values)
                    median = np.median(xdata.values)
                    MeanWellsReplicas.setdefault(well, []).append(mean)
                    MedianWellsReplicas.setdefault(well, []).append(median)
                    SdCells[well] = np.std(xdata.values)
                    MadCells[well] = TCA.mad(xdata.values)
                    MeanCells[well] = mean
                    MedianCells[well] = median
                ResultatsArray.add_data(PercentCells, chan, str(replica.name)+'_PosCells')
                ResultatsArray.add_data(MeanCells, chan, str(replica.name)+'_Mean')
                ResultatsArray.add_data(SdCells, chan, str(replica.name)+"_Std")
                ResultatsArray.add_data(MedianCells, chan, str(replica.name)+'_Median')
                ResultatsArray.add_data(MadCells, chan, str(replica.name)+"_Mad")


            ########### P-VALUE AND FDR ON % OF POSITIVE CELLS
            if neg is not None:
                if len(plate) > 1:
                    log.debug("Perform T-Test on positive Cells percentage")
                    NegData = list()
                    for x in neg_well:
                        NegData.extend(PercentCellsReplicas[x])
                    ## or this but don't work when data are missing ????
                    # neg_data = [PercentCellsReplicas[x] for x in neg_well]
                    NegData = np.array(NegData).flatten()
                    pvalue = {}
                    for key, value in PercentCellsReplicas.items():
                        x = stats.ttest_ind(value, NegData, equal_var=False)
                        pvalue[key] = x[1]

                    ResultatsArray.add_data(pvalue, chan, 'PosCells p-value')
                    ResultatsArray.values.loc[:, (chan, "PosCells fdr")] = TCA.adjustpvalues(pvalues=ResultatsArray.values.loc[:, (chan, "PosCells p-value")])

            ########### VARIABILITY
            Mean = dict([(i, sum(v) / len(v)) for i, v in MeanWellsReplicas.items()])
            Median = dict([(i, sum(v) / len(v)) for i, v in MedianWellsReplicas.items()])
            ResultatsArray.add_data(Mean, chan, 'Mean')
            ResultatsArray.add_data(Median, chan, 'Median')

            if len(plate) > 1:
                log.debug("Variability determination")
                MeanSD = dict([(i, np.std(v)) for i, v in MeanWellsReplicas.items()])
                MedianSD = dict([(i, np.std(v)) for i, v in MedianWellsReplicas.items()])
                ResultatsArray.add_data(MeanSD, chan, 'Mean std')
                ResultatsArray.add_data(MedianSD, chan, 'Median std')

            ########### POSITIVE CELLS
            # determine the mean of replicat
            MeanPercentCells = dict([(i, sum(v) / len(v)) for i, v in PercentCellsReplicas.items()])
            ResultatsArray.add_data(MeanPercentCells, chan, 'PositiveCells')

            # ########## determine the standart deviation of % Cells
            if len(plate) > 1:
                for key, value in PercentCellsReplicas.items():
                    PercentCellsSDReplicas[key] = np.std(value)

                ResultatsArray.add_data(PercentCellsSDReplicas, chan, 'PositiveCells std')

            # ########## toxicity index
            if neg is not None:
                log.debug("Toxicity determination")
                # ### 0 idx is the max cell of all plate
                # max_cell = max(MeanCellsCount.values())
                # ### 0 idx is the neg control
                temp = list()
                for neg in neg_well:
                    try:
                        temp.extend(CellsCountReplicas[neg])
                    except Exception as e:
                        pass
                max_cell = np.mean(temp)
                ## or this but don't work when data are missing ????
                # max_cell = np.mean([CellsCountReplicas[neg] for neg in neg_well])
                min_cell = min(MeanCellsCount.values())
                ToxIdx = {}
                for key, item in MeanCellsCount.items():
                    ToxIdx[key] = (max_cell - item) / (max_cell - min_cell)

                ResultatsArray.add_data(ToxIdx, chan, 'Toxicity')

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

                    ResultatsArray.add_data(Viability, chan, 'Viability')
                else:
                    log.info('  No positive control provided, no viability performed')

    ### Remove row with cellscount is 0
    if clean:
        ResultatsArray.values = ResultatsArray.values[ResultatsArray.values["Plate"]["CellsCount"] > 0]

    ## FINISH RETURN RESULT
    if channels is not None:
        return ResultatsArray.values, ThresholdVALUE
    else:
        return ResultatsArray.values

class Result(object):
    """
    Class Result is especially created for plateAnalyzis.
    This class store data with dict in input, where key are well and item are data.
    """

    def __init__(self, plate):
        """
        Constructor
        :return: dataframe
        """
        assert isinstance(plate, TCA.Plate)

        __SIZE__ = plate.platemap.shape(alt_frmt=True)

        tmp = pd.DataFrame(plate.platemap.as_array())
        tmp.columns = [['Plate', 'Plate'], ['Well', 'PlateMap']]
        self.values = pd.concat([pd.DataFrame(np.repeat([plate.name], 96), columns=[['Plate'], ['PlateName']]),
                        tmp],
                        axis=1)

    def add_data(self, datadict, chan, col):
        """
        Insert Value from a dict where key = GeneName/pos and Value are value to insert
        :param datadict: dict that contain value to insert with key are GeneName or Pos/Well
        :param chan: plate or channel analyzed
        :param col: columns name to insert data
        """
        try:
            x = pd.DataFrame.from_dict(datadict, orient='index').reset_index()
            x.columns = [np.array(['Plate', str(chan)]), np.array(['Well', str(col)])]
            self.values = pd.merge(self.values, x, how='outer')
        except Exception as e:
            print(e)
