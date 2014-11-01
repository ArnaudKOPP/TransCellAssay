"""
Positive cell count method
"""

import numpy as np
import Core
import Utils.WellFormat

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def getPercentPosCell(plate, feature, control, threshold, direction, verbose=False):
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

    try:
        if isinstance(plate, Core.Plate):
            replicat_Dict = plate.getAllReplicat()
            ps = plate.PlateSetup
            control_well = ps.getGeneWell(control)
            # iterate on replicat dict
            for k, replicat in replicat_Dict.items():
                # # threshold value for control
                data_control = replicat.getDataByWells(control_well, feature=feature)
                threshold_value = np.percentile(data_control, threshold)
                # data from replicat
                data = replicat.Dataframe
                # get all well from data
                well_list = data.Well.unique()

                df_groupby = data.groupby("Well")

                # iterate on well
                for well in well_list:
                    # # Take long time here ~ 130 ms
                    xdata = df_groupby.get_group(well)
                    len_total = len(xdata)
                    if direction == 'Up':
                        len_thres = len(np.extract(xdata > threshold_value, xdata))
                    else:
                        len_thres = len(np.extract(xdata < threshold_value, xdata))
                    # # include in dict key is the position and value is a %
                    dict_percent_cell_tmp.setdefault(well, []).append(((len_thres / len_total) * 100))
            # determine the mean of replicat
            dict_percent_cellList = [(i, sum(v) / len(v)) for i, v in dict_percent_cell_tmp.items()]
            dict_percent_cell = dict(dict_percent_cellList)
            # determine the standart deviation of % Cells
            try:
                for key, value in dict_percent_cell_tmp.items():
                    dict_percent_sd_cell[key] = np.std(value)
            except Exception as e:
                print(e)

            if verbose:
                mean = np.zeros(plate.PlateSetup.platesetup.shape)
                sd = np.zeros(plate.PlateSetup.platesetup.shape)

                for k, v in dict_percent_cell.items():
                    well = Utils.WellFormat.getOppositeWellFormat(k)
                    mean[well[0]][well[1]] = v

                for k, v in dict_percent_sd_cell.items():
                    well = Utils.WellFormat.getOppositeWellFormat(k)
                    sd[well[0]][well[1]] = v

                print("Mean of number of Cells for given Threshold by well : ")
                print(mean)
                print("Standart deviation of number of Cells for given Threshold by Well : ")
                print(sd)

            return dict_percent_cell, dict_percent_sd_cell
        else:
            raise TypeError
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)