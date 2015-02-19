# coding=utf-8
"""
Compute basics score for plate and store result into a Result object.
Compute Cells Count, percent of positive Cells, viability and toxicity per Wells.
"""

import TransCellAssay as TCA
import numpy as np
import pandas as pd
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


def plate_analysis(plate, channel, neg, pos, threshold=50, percent=True):
    """
    Do a plate analysis
    :param plate: plate
    :param channel: reference channel
    :param neg: negative control
    :param pos: positive control
    :param threshold: threshold for defining % of positive cell in negative ref
    :param percent: use percent for threshold, if false, it will be a real value
    :return: return result
    """
    if not isinstance(plate, TCA.Plate):
        raise TypeError("File Plate Object")
    else:
        if plate._is_cutted:
            log.error('Plate was cutted, for avoiding undesired effect, plate analysis cannot be performed')
            raise NotImplementedError()
        log.info('Perform plate analysis : {}'.format(plate.name))
        platemap = plate.get_platemap()
        size = platemap.shape()
        result = Result(size=(size[0] * size[1]))
        x = platemap.as_dict()
        result.init_gene_well(x)

        neg_well = plate.platemap.search_well(neg)
        pos_well = plate.platemap.search_well(pos)

        cell_count_tmp = {}
        mean = {}
        median = {}
        dict_percent_cell_tmp = {}
        dict_percent_sd_cell = {}

        # # iterate over replicat
        for k, replica in plate.replica.items():
            # # cell count
            datagb = replica.rawdata.get_groupby_data()
            cellcount = datagb.Well.count().to_dict()
            for key, value in cellcount.items():
                try:
                    cell_count_tmp.setdefault(key, []).append(value)
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
                mean.setdefault(well, []).append(np.mean(xdata.values))
                median.setdefault(well, []).append(np.median(xdata.values))
                len_total = len(xdata.values)
                len_thres = len(np.extract(xdata.values > threshold_value, xdata.values))
                # # include in dict key is the position and value is a %
                dict_percent_cell_tmp.setdefault(well, []).append(((len_thres / len_total) * 100))

        # # Cell count and std
        sdvalue = {}
        for key, value in cell_count_tmp.items():
            sdvalue[key] = np.std(value)
        meancountlist = [(i, sum(v) / len(v)) for i, v in cell_count_tmp.items()]
        meancount = dict(meancountlist)  # # convert to dict

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
        std = [(i, np.std(v)) for i, v in mean.items()]
        stdm = [(i, np.std(v)) for i, v in median.items()]
        std = dict(std)
        stdm = dict(stdm)

        mean = [(i, sum(v) / len(v)) for i, v in mean.items()]
        median = [(i, sum(v) / len(v)) for i, v in median.items()]
        mean = dict(mean)
        median = dict(median)

        result.add_data(mean, 'Mean')
        result.add_data(median, 'Median')
        result.add_data(std, 'Std')
        result.add_data(stdm, 'Stdm')

        # # positive cell
        # determine the mean of replicat
        dict_percent_celllist = [(i, sum(v) / len(v)) for i, v in dict_percent_cell_tmp.items()]
        dict_percent_cell = dict(dict_percent_celllist)

        # determine the standart deviation of % Cells
        for key, value in dict_percent_cell_tmp.items():
            dict_percent_sd_cell[key] = np.std(value)

        result.add_data(dict_percent_cell, 'PositiveCells')
        result.add_data(dict_percent_sd_cell, 'SDPositiveCells')

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
        self.values = np.zeros(size, dtype=[('GeneName', object), ('Well', object), ('CellsCount', float),
                                            ('SDCellsCount', float), ('PositiveCells', float),
                                            ('SDPositiveCells', float), ('Mean', float), ('Std', float),
                                            ('Median', float), ('Stdm', float), ('Viability', float),
                                            ('Toxicity', float)])

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