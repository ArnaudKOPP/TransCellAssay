# coding=utf-8
"""
Compute basics score for plate and store result into a Result object.
Compute Cells Count, percent of positive Cells, viability and toxicity per Wells.
"""

import TransCellAssay as TCA
import numpy as np
import pandas as pd
import collections
import os
from scipy import stats
import logging
log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def plate_analysis(plate, channel, neg, pos, threshold=50, percent=True, path=None, supp_data=False):
    """
    Do a plate analysis
    :param plate: plate
    :param channel: reference channel
    :param neg: negative control
    :param pos: positive control
    :param threshold: threshold for defining % of positive cell in negative ref
    :param percent: use percent for threshold, if false, it will be a real value
    :param path: Path to save Data
    :param supp_data: Saving supp data if path is not None
    :return: return result
    """
    if not isinstance(plate, TCA.Plate):
        raise TypeError("File Plate Object")
    else:
        if threshold >= 100 and percent:
            log.warning('Threshold cannot be > 100 with percent')
            percent = False

        if plate._is_cutted:
            log.error('Plate was cutted, for avoiding undesired effect, plate analysis cannot be performed')
            raise NotImplementedError()
        log.info('Perform plate analysis for {0} on channel {1}'.format(plate.name, channel))

        platemap = plate.get_platemap()

        size = platemap.shape()
        __SIZE__ = (size[0] * size[1])

        result = Result(size=__SIZE__)
        x = platemap.as_dict()

        result.init_gene_well(x)
        result.values['Plate'] = np.repeat([plate.name], __SIZE__)

        neg_well = plate.platemap.search_well(neg)
        pos_well = plate.platemap.search_well(pos)

        cell_count_all_replica = collections.OrderedDict()
        mean_well_value_all_replica = collections.OrderedDict()
        median_well_value_all_replica = collections.OrderedDict()
        percent_cell_all_replica = collections.OrderedDict()
        percent_cell_sd = collections.OrderedDict()

        def __dict_to_df(input_dict):
            name = np.array(list(input_dict))
            name = name.flatten().reshape(len(name), 1)
            ar = np.concatenate(list(input_dict.values()))
            ar = ar.flatten().reshape(len(ar)/len(plate.replica), len(plate.replica))
            ar = np.append(ar, name, axis=1)
            return pd.DataFrame(ar)

        # # iterate over replicat
        for k, replica in plate.replica.items():
            log.debug("PlateAnalysis : iteration on rep %s" % replica.name)
            # # cell count
            datagb = replica.rawdata.get_groupby_data()
            cellcount = datagb.Well.count().to_dict()
            for key, value in cellcount.items():
                try:
                    cell_count_all_replica.setdefault(key, []).append(value)
                except KeyError:
                    pass

            # # positive Cell
            # # threshold value for control
            if percent:
                data_control = replica.get_raw_data(channel=channel, well=neg_well)
                threshold_value = np.percentile(data_control, threshold)
            else:
                threshold_value = threshold

            # # variability
            well_list = replica.rawdata.get_unique_well()
            # iterate on well
            for well in well_list:
                xdata = datagb.get_group(well)[channel]
                mean_well_value_all_replica.setdefault(well, []).append(np.mean(xdata.values))
                median_well_value_all_replica.setdefault(well, []).append(np.median(xdata.values))
                len_total = len(xdata.values)
                len_thres = len(np.extract(xdata.values > threshold_value, xdata.values))
                # # include in dict key is the position and value is a %
                percent_cell_all_replica.setdefault(well, []).append(((len_thres / len_total) * 100))

        # p-value and fdr for percent cell
        neg_data = [percent_cell_all_replica[x] for x in neg_well]
        neg_data = np.array(neg_data).flatten()
        pvalue = collections.OrderedDict()
        for key, value in percent_cell_all_replica.items():
            x = stats.ttest_ind(value, neg_data, equal_var=False)
            pvalue[key] = x[1]

        result.add_data(pvalue, 'p-value')
        result.values["fdr"] = TCA.adjustpvalues(pvalues=result.values["p-value"])

        # # Cell count and std
        sdvalue = {}
        for key, value in cell_count_all_replica.items():
            sdvalue[key] = np.std(value)
        meancount = dict([(i, sum(v) / len(v)) for i, v in cell_count_all_replica.items()])

        result.add_data(meancount, 'CellsCount')
        result.add_data(sdvalue, 'SDCellsCount')

        # # toxicity index
        max_cell = max(meancount.values())
        min_cell = min(meancount.values())
        txidx = {}
        for key, item in meancount.items():
            txidx[key] = (max_cell - item) / (max_cell - min_cell)

        # # viability index
        neg_val = [meancount[x] for x in neg_well]
        pos_val = [meancount[x] for x in pos_well]
        viability = {}
        for key, item in meancount.items():
            viability[key] = (item - np.mean(pos_val) - 3 * np.std(pos_val)) / np.abs(
                np.mean(neg_val) - np.mean(pos_val))

        result.add_data(txidx, 'Toxicity')
        result.add_data(viability, 'Viability')

        # # variability
        std = dict([(i, np.std(v)) for i, v in mean_well_value_all_replica.items()])
        stdm = dict([(i, np.std(v)) for i, v in median_well_value_all_replica.items()])

        mean_well_value_all_replica = dict([(i, sum(v) / len(v)) for i, v in mean_well_value_all_replica.items()])
        median_well_value_all_replica = dict([(i, sum(v) / len(v)) for i, v in median_well_value_all_replica.items()])

        result.add_data(mean_well_value_all_replica, 'Mean')
        result.add_data(median_well_value_all_replica, 'Median')
        result.add_data(std, 'Std')
        result.add_data(stdm, 'Stdm')

        # # positive cell
        # determine the mean of replicat
        dict_percent_cell = dict([(i, sum(v) / len(v)) for i, v in percent_cell_all_replica.items()])

        # determine the standart deviation of % Cells
        for key, value in percent_cell_all_replica.items():
            percent_cell_sd[key] = np.std(value)

        result.add_data(dict_percent_cell, 'PositiveCells')
        result.add_data(percent_cell_sd, 'SDPositiveCells')

        if path is not None:
            try:
                result.write(file_path=os.path.join(path, 'PlateAnalyzisData_'+str(plate.name)+'.csv'))
            except Exception as e:
                log.error('Error during save PlateAnalyzisData : {}'.format(e))

        if supp_data:
            writer = pd.ExcelWriter(os.path.join(path, 'SUPP_DATA_'+str(plate.name)+'.xlsx'))
            try:
                percent = __dict_to_df(percent_cell_all_replica)
                cellcnt = __dict_to_df(cell_count_all_replica)
                percent.to_excel(writer, 'Percent Cells', index=None, header=None)
                cellcnt.to_excel(writer, 'Cells Count', index=None, header=None)
            except Exception as e:
                log.error('Error with SUPP_DATA export : {}'.format(e))

            writer.save()
        return result


class Result(object):
    """
    Class Result is especialy created for plateAnalyzis.
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
        self.values = np.zeros(size, dtype=[('Plate', object), ('GeneName', object), ('Well', object),
                                            ('CellsCount', float), ('SDCellsCount', float), ('PositiveCells', float),
                                            ('SDPositiveCells', float), ('p-value', float), ('fdr', float),
                                            ('Mean', float), ('Std', float), ('Median', float), ('Stdm', float),
                                            ('Viability', float), ('Toxicity', float)])

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
                self.values['GeneName'][i] = v
                self.values['Well'][i] = k
                self._genepos_genename[k] = i
                i += 1
        except Exception as e:
            print(e)

    def add_data(self, datadict, col):
        """
        Insert Value from a dict where key = GeneName/pos and Value are value to insert
        Prefer by = pos in case of empty well
        :param datadict: dict that contain value to insert with key are GeneName or Pos/Well
        :param col: colname to insert data
        """
        try:
            for item, value in datadict.items():
                self.values[col][self._genepos_genename[item]] = value
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