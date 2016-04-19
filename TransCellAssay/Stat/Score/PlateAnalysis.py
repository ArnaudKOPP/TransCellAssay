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
            if isinstance(threshold, dict):
                THRES = threshold[chan]
            else:
                THRES = threshold

            if THRES >= 100 and percent:
                log.warning('Threshold cannot be > 100 in %')
                percent = False
                fixed_threshold = True

            for repName, replica in plate:
                datagb = replica.get_groupby_data()

                if fixed_threshold:
                    ThresholdValue = THRES
                else:
                    ControlData = replica.get_rawdata(channel=chan, well=neg_well)
                    if percent:
                        ThresholdValue = np.percentile(ControlData, THRES)
                    else:
                        # Take mean of neg ctrl if fixed_threshold and percent are False
                        ThresholdValue = np.mean(ControlData)

                ThresholdVALUE[chan][repName] = ThresholdValue

    return ThresholdVALUE


def PlateChannelsAnalysis(plate, channels=None, neg=None, pos=None, threshold=50, percent=True, fixed_threshold=False,
                          clean=False,noposcell=False, multiIndexDF=False):
    """
    Do a plate analysis for multiple channels and parameters
    :param plate: plate object
    :param channel: list of channels to analyse
    :param neg: negative control
    :param pos: positive control, is optional
    :param threshold: fixe the percent of positive well found in negative control well
    :param percent: True if threshold value is percent, False if we want to give a value
    :param fixed_threshold: use given threshold (value mode) for all well
    :param clean: if True, remove all row/Well that don't contain cells
    :param noposcell: If we don't want to compute positive cells %
    :param multiIndexDF: if True, give the dataframe with multiindex level
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
    NREP = len(plate)

    ## this array is a basic array for begin some calculations
    __array_pattern = pd.DataFrame(plate.platemap.as_array())

    COUNT = __array_pattern.copy()
    COUNT.loc[:, 'PlateName'] = np.repeat([plate.name], SIZE)

    ######################### CELLS COUNT

    for replicaId, replica in plate:
        cellcount = replica.get_groupby_data()[__WellKey].count()
        cellcount.name = replicaId+" CellsCount"
        COUNT = pd.merge(COUNT, cellcount.reset_index(), how='left', on=__WellKey)

    COUNT.loc[:, "CellsCount Mean"] = COUNT.iloc[:, -NREP:].mean(axis=1)
    COUNT.loc[:, "CellsCount Std"] = COUNT.iloc[:, -NREP:].std(axis=1)


    ########### TOXICITY IF NEG IS GIVEN

    if neg is not None:

        neg_count = COUNT[COUNT.loc[:, "PlateMap"] == neg].iloc[:, 3:3+NREP]

        tmp = COUNT.iloc[:, 3:3+NREP].copy()
        tmp.columns = [i+" ToxIdx" for i in tmp.columns]

        for i in range(NREP):
            tmp.iloc[:, i] = (tmp.iloc[:, i] / np.mean(neg_count.iloc[:, i])) * 100

        COUNT = pd.concat([COUNT, tmp], axis=1)

        COUNT.loc[:, "Tox mean"] = COUNT.iloc[:, -NREP:].mean(axis=1)
        COUNT.loc[:, "Tox std"] = COUNT.iloc[:, -NREP-1:-1].std(axis=1)

        if NREP > 1:
            negdata = COUNT[COUNT.loc[:, "PlateMap"] == neg].loc[:, "Tox mean"].values
            COUNT.loc[:, "Tox pvalue"] = COUNT.iloc[:, -NREP-2: -2].apply((lambda x: stats.ttest_ind(x, negdata, equal_var=False)[1]), axis=1)
            COUNT.loc[:, "Tox fdr"] = TCA.adjustpvalues(pvalues = COUNT.loc[:, "Tox pvalue"])

    ##################### ANALYSING CHANNELS
    DF = []
    if channels is not None:
        log.info('Perform plate analysis for {0} plate on channels :{1}'.format(plate.name, channels))
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

        if noposcell is False:
            ThresholdVALUE = getThreshold(plate, ctrl=neg, channels=channels, threshold=threshold, percent=percent,
                            fixed_threshold=fixed_threshold)
            log.debug("Threshold used : {}".format(ThresholdVALUE))

        ## iterate over channels
        for chan in channels:
            MEAN = __array_pattern.copy()
            MEDIAN = __array_pattern.copy()
            STD = __array_pattern.copy()
            MAD = __array_pattern.copy()
            if noposcell is False:
                PERCENT = __array_pattern.copy()


            for replicaId, replica in plate:
                datagb = replica.get_groupby_data()
                if noposcell is False:
                    ########### POSITIVE CELLS %
                    # # threshold value for control
                    ThresholdValue = ThresholdVALUE[chan][replicaId]

                ########### VARIABILITY & % OF POSITIVE CELLS
                # iterate on well
                if noposcell is False:
                    PercentCells = {}
                MeanCells = {}
                MedianCells = {}
                SdCells = {}
                MadCells = {}

                for well in replica.get_unique_well():
                    xdata = datagb.get_group(well)[chan]
                    if noposcell is False:
                        len_total = len(xdata.values)
                        len_thres = len(np.extract(xdata.values > ThresholdValue, xdata.values))
                        # # include in dict key is the position and value is a %
                        PercentCells[well] = (len_thres / len_total) * 100
                    SdCells[well] = np.std(xdata.values)
                    MadCells[well] = TCA.mad(xdata.values)
                    MeanCells[well] = np.mean(xdata.values)
                    MedianCells[well] = np.median(xdata.values)

                mean = pd.DataFrame.from_dict(MeanCells, orient='index').reset_index()
                mean.columns = [__WellKey, replicaId+" Mean"]
                MEAN = pd.merge(MEAN, mean, how='left', on=__WellKey)

                median = pd.DataFrame.from_dict(MedianCells, orient='index').reset_index()
                median.columns = [__WellKey, replicaId+" Median"]
                MEDIAN = pd.merge(MEDIAN, median, how='left', on=__WellKey)

                std = pd.DataFrame.from_dict(SdCells, orient='index').reset_index()
                std.columns = [__WellKey, replicaId+" Std"]
                STD = pd.merge(STD, std, how='left', on=__WellKey)

                mad = pd.DataFrame.from_dict(MadCells, orient='index').reset_index()
                mad.columns = [__WellKey, replicaId+" Mad"]
                MAD = pd.merge(MAD, mad, how='left', on=__WellKey)

                if noposcell is False:
                    percent = pd.DataFrame.from_dict(PercentCells, orient='index').reset_index()
                    percent.columns = [__WellKey, replicaId+" PosCells"]
                    PERCENT = pd.merge(PERCENT, percent, how='left', on=__WellKey)


            MEAN.loc[:, "Mean mean"] = MEAN.iloc[:, -NREP:].mean(axis=1)
            MEDIAN.loc[:, "Median mean"] = MEDIAN.iloc[:, -NREP:].mean(axis=1)
            if noposcell is False:
                PERCENT.loc[:, "PosCells mean"] = PERCENT.iloc[:, -NREP:].mean(axis=1)

            if NREP > 1:
                MEAN.loc[:, "Mean std"] = MEAN.iloc[:, -NREP-1:-1].std(axis=1)
                MEDIAN.loc[:, "Median mad"] = MEDIAN.iloc[:, -NREP-1:-1].mad(axis=1)
                if noposcell is False:
                    PERCENT.loc[:, "PosCells std"] = PERCENT.iloc[:, -NREP-1: -1].std(axis=1)


            if noposcell is False:
                ########### P-VALUE AND FDR ON % OF POSITIVE CELLS
                if neg is not None:
                    if NREP > 1:
                        NegData = np.concatenate(PERCENT[PERCENT.loc[:, "PlateMap"] == neg].iloc[:, -NREP-2:-2].values).flatten()
                        pvalue = PERCENT.iloc[:, -NREP-2: -2].apply((lambda x: stats.ttest_ind(x, NegData, equal_var=False)[1]), axis=1)
                        PERCENT.loc[:, "PosCells pvalue"] = pvalue
                        PERCENT.loc[:, "PosCells fdr"] = TCA.adjustpvalues(pvalues=PERCENT.loc[:, "PosCells pvalue"])

                PERCENT.loc[:, "PosCells Zscore"] = (PERCENT.loc[:, 'PosCells mean'] - PERCENT.loc[:, 'PosCells mean'].mean())/PERCENT.loc[:, 'PosCells mean'].std()

            ### ADD CHANNEL ON TOP OF DF
            if noposcell is False:
                df = pd.concat([MEAN.iloc[:, 2:], STD.iloc[:, 2:], MEDIAN.iloc[:, 2:],
                                MAD.iloc[:, 2:], PERCENT.iloc[:, 2:]], axis=1)
            else:
                df = pd.concat([MEAN.iloc[:, 2:], STD.iloc[:, 2:], MEDIAN.iloc[:, 2:],
                                MAD.iloc[:, 2:]], axis=1)

            if multiIndexDF:
                df.columns = pd.MultiIndex.from_tuples([tuple([chan, c]) for c in df.columns])
            else:
                df.columns = [str(chan)+" "+col for col in df.columns]
            DF.append(df)

    ########### FINAL OPERATION

    if multiIndexDF:
        COUNT.columns = pd.MultiIndex.from_tuples([tuple(["Plate", c]) for c in COUNT.columns])

    if neg is not None or channels is not None:
        result = pd.concat([COUNT, pd.concat(DF, axis=1)], axis=1)
    else:
        result = COUNT

    ### Remove row with cellscount is 0
    if clean:
        result = result[result["Plate"]["CellsCount Mean"] > 0]


    if channels is not None:
        if noposcell is False:
            return result, ThresholdVALUE
        else:
            return result
    else:
        return result
