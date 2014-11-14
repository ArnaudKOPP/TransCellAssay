"""
Count Positive Cell in each well, the threshold is given by the % of positive cell in negative control
"""

import numpy as np
import TransCellAssay as TCA

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def getPercentPosCell(plate, feature, control, threshold, verbose=False):
    """
    get % of Cell over threshold, default threshold is 50%
    This function take some time and need to be very improve
    :param plate:
    :param feature: on which feature
    :param threshold: threshold that defined % of pos cell into negative reference
    :param direction: Up effect or down effect
    :return: return a dict with mean % of pos Cell and standart variation across replicat
    """
    dict_percent_cell = {}
    dict_percent_cell_tmp = {}
    dict_percent_sd_cell = {}
    if not isinstance(plate, TCA.Core.Plate):
        raise TypeError("\033[0;31m[ERROR]\033[0m  Take a Plate object in input")
    else:
        replicat_Dict = plate.getAllReplicat()
        pm = plate.PlateMap
        control_well = pm.getGeneWell(control)

        # iterate on replicat dict
        for k, replicat in replicat_Dict.items():
            # # threshold value for control
            data_control = replicat.getDataByWells(control_well, feature=feature)
            threshold_value = np.percentile(data_control, threshold)
            # data from replicat
            data = replicat.Dataframe
            datagroupby = data.groupby('Well')

            # get all well from data
            well_list = data.Well.unique()
            # iterate on well
            for well in well_list:
                # # Take long time here ~ 130 ms
                # xdata = data[feature][data['Well'] == well]
                xdata = datagroupby.get_group(well)[feature]
                len_total = len(xdata)
                len_thres = len(np.extract(xdata > threshold_value, xdata))
                # # include in dict key is the position and value is a %
                dict_percent_cell_tmp.setdefault(well, []).append(((len_thres / len_total) * 100))

        # determine the mean of replicat
        dict_percent_cellList = [(i, sum(v) / len(v)) for i, v in dict_percent_cell_tmp.items()]
        dict_percent_cell = dict(dict_percent_cellList)

        # determine the standart deviation of % Cells
        for key, value in dict_percent_cell_tmp.items():
            dict_percent_sd_cell[key] = np.std(value)

        if verbose:
            mean = np.zeros(plate.PlateMap.platemap.shape)
            sd = np.zeros(plate.PlateMap.platemap.shape)

            for k, v in dict_percent_cell.items():
                well = TCA.Utils.WellFormat.getOppositeWellFormat(k)
                mean[well[0]][well[1]] = v

            for k, v in dict_percent_sd_cell.items():
                well = TCA.Utils.WellFormat.getOppositeWellFormat(k)
                sd[well[0]][well[1]] = v

            print("Mean of number of Cells for given Threshold by well : ")
            print(mean)
            print("Standart deviation of number of Cells for given Threshold by Well : ")
            print(sd)

        return dict_percent_cell, dict_percent_sd_cell
