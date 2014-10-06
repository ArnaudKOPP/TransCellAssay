__author__ = 'Arnaud KOPP'
import numpy as np
import pandas as pd
import TCA


def getPercentPosCell(plate, feature, control, threshold=50, direction='Up'):
    '''
    get % of Cell over threshold, default threshold is 50%
    :param plate:
    :param feature: on which feature
    :param threshold:
    :param direction: Up effect or down effect
    :return: return a dict with mean % of pos Cell and standart variation across replicat
    '''
    dict_percent_cell = {}
    dict_percent_sd_cell = {}

    try:
        if isinstance(plate, TCA.Plate):
            replicat_Dict = plate.getAllReplicat()
            ps = plate.PlateSetup
            control_well = ps.getGeneWell(control)
            # iterate on replicat dict
            for k, replicat in replicat_Dict.items():
                ## threshold value for control
                data_control = replicat.getDataByWells(feature, control_well)
                threshold_value = np.percentile(data_control, threshold)
                # data from replicat
                data = replicat.Data
                # get all well from data
                well_list = data.Well.unique()

                # iterate on well
                for well in well_list:
                    xdata = data[feature][data['Well'] == well]
                    len_total = len(xdata)
                    if direction == 'Up':
                        len_thres = len(np.extract(xdata > threshold_value, xdata))
                    else:
                        len_thres = len(np.extract(xdata < threshold_value, xdata))
                    ## include in dict key is the position and value is a %
                    dict_percent_cell.setdefault(well, []).append(((len_thres / len_total) * 100))
            # determine the standart deviation of % Cells
            try:
                for key, value in dict_percent_cell.items():
                    dict_percent_sd_cell[key] = np.std(value)
            except Exception as e:
                print(e)
            return dict_percent_cell, dict_percent_sd_cell
        else:
            raise TypeError
    except Exception as e:
        print(e)