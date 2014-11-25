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


def get_percent_positive_cell(plate, feature, control, threshold):
    """
    get % of Cell over threshold, default threshold is 50%
    This function take some time and need to be very improve
    :param plate:
    :param feature: on which feature
    :param threshold: threshold that defined % of pos cell into negative reference
    :return: return a dict with mean % of pos Cell and standart variation across replicat
    """
    try:
        dict_percent_cell = {}
        dict_percent_cell_tmp = {}
        dict_percent_sd_cell = {}
        if not isinstance(plate, TCA.Core.Plate):
            raise TypeError("\033[0;31m[ERROR]\033[0m  Take a Plate object in input")
        else:
            replicat_dict = plate.get_all_replicat()
            pm = plate.PlateMap
            control_well = pm.get_well(control)

            # iterate on replicat dict
            for k, replicat in replicat_dict.items():
                # # threshold value for control
                data_control = replicat.get_raw_data_by_wells(control_well, feature=feature)
                threshold_value = np.percentile(data_control, threshold)
                # data from replicat
                datagroupby = replicat.RawData.groupby('Well')

                # iterate on well
                for well in replicat.RawData.Well.unique():
                    xdata = datagroupby.get_group(well)[feature]
                    len_total = len(xdata)
                    len_thres = len(np.extract(xdata > threshold_value, xdata))
                    # # include in dict key is the position and value is a %
                    dict_percent_cell_tmp.setdefault(well, []).append(((len_thres / len_total) * 100))

            # determine the mean of replicat
            dict_percent_celllist = [(i, sum(v) / len(v)) for i, v in dict_percent_cell_tmp.items()]
            dict_percent_cell = dict(dict_percent_celllist)

            # determine the standart deviation of % Cells
            for key, value in dict_percent_cell_tmp.items():
                dict_percent_sd_cell[key] = np.std(value)

            return dict_percent_cell, dict_percent_sd_cell
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)
