"""
Compute basics score for plate and store result into a Result object
"""

import TransCellAssay
import numpy as np

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def compute_plate_analyzis(plate, feature, neg, pos, threshold=50):
    """
    Compute all score/carac implemented before, for plate
    :param plate: Plate object
    :param feature: which feature to analyze
    :param neg: negative control reference
    :param pos: positive control reference
    :param threshold: threshold for defining % of positive cell in negative ref
    :return: return a result object
    """
    try:
        if isinstance(plate, TransCellAssay.Plate):
            platemap = plate.get_platemap()
            size = platemap.get_platemape_shape()
            result = TransCellAssay.Result(size=(size[0] * size[1]))
            x = platemap.get_map_as_dict()
            result.init_gene_well(x)
            try:
                meancount, sdvalue = TransCellAssay.get_cell_count(plate)
                percentcell, sdpercentcell = TransCellAssay.get_percent_positive_cell(plate, feature, neg, threshold)
                mean, median, std, stdm = TransCellAssay.get_variability(plate, feature)
                toxicity, viability = TransCellAssay.get_toxicity_viability(plate=plate, cell_count=meancount, neg=neg,
                                                                            pos=pos)

                # Add all result into Result Data Frame
                result.add_data(meancount, 'CellsCount')
                result.add_data(sdvalue, 'SDCellsCunt')
                result.add_data(percentcell, 'PositiveCells')
                result.add_data(sdpercentcell, 'SDPositiveCells')
                result.add_data(mean, 'Mean')
                result.add_data(median, 'Median')
                result.add_data(std, 'Std')
                result.add_data(stdm, 'Stdm')
                result.add_data(toxicity, 'Toxicity')
                result.add_data(viability, 'Viability')

                return result
            except Exception as e:
                print(e)
        else:
            raise TypeError("\033[0;31m[ERROR]\033[0m Input Plate Object")
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)


def plate_analysis(plate, feature, neg, pos, threshold=50):
    """
    Do a plate analysis
    :param plate: plate
    :param feature: reference feature
    :param neg: negative control
    :param pos: positive control
    :param threshold: threshold for defining % of positive cell in negative ref
    :return: return result
    """
    try:
        if isinstance(plate, TransCellAssay.Plate):
            platemap = plate.get_platemap()
            size = platemap.get_platemape_shape()
            result = TransCellAssay.Result(size=(size[0] * size[1]))
            x = platemap.get_map_as_dict()
            result.init_gene_well(x)

            neg_well = plate.PlateMap.get_well(neg)
            pos_well = plate.PlateMap.get_well(pos)

            cell_count_tmp = {}
            mean = {}
            median = {}
            dict_percent_cell = {}
            dict_percent_cell_tmp = {}
            dict_percent_sd_cell = {}

            # # iterate over replicat
            for k, v in plate.replicat.items():
                # # cell count
                datagp = v.RawData.groupby("Well")
                cellcount = datagp.Well.count().to_dict()
                for key in cellcount.keys():
                    try:
                        cell_count_tmp.setdefault(key, []).append(cellcount[key])
                    except KeyError:
                        pass

                # # variability
                well_list = v.RawData.Well.unique()
                # iterate on well
                for well in well_list:
                    mean.setdefault(well, []).append(np.mean(datagp.get_group(well)[feature]))
                    median.setdefault(well, []).append(np.median(datagp.get_group(well)[feature]))

                # # positive Cell
                # # threshold value for control
                data_control = v.get_raw_data_by_wells(neg_well, feature=feature)
                threshold_value = np.percentile(data_control, threshold)
                # data from replicat
                datagroupby = v.RawData.groupby('Well')

                # iterate on well
                for well in v.RawData.Well.unique():
                    xdata = datagroupby.get_group(well)[feature]
                    len_total = len(xdata)
                    len_thres = len(np.extract(xdata > threshold_value, xdata))
                    # # include in dict key is the position and value is a %
                    dict_percent_cell_tmp.setdefault(well, []).append(((len_thres / len_total) * 100))

            # # Cell count and std
            sdvalue = {}
            for key, value in cell_count_tmp.items():
                sdvalue[key] = np.std(value)
            meancountlist = [(i, sum(v) / len(v)) for i, v in cell_count_tmp.items()]
            meancount = dict(meancountlist)  # # convert to dict

            result.add_data(meancount, 'CellsCount')
            result.add_data(sdvalue, 'SDCellsCunt')

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
        else:
            raise TypeError("\033[0;31m[ERROR]\033[0m Input Plate Object")
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)