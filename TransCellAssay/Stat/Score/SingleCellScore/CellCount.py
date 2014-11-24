"""
Cell count method
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


def get_cell_count(plate, verbose=False):
    """
    get mean of number of cell per well accross replicat
    :param plate : Give a TCA.Plate object
    :return: return a dict that contain mean value for well, with well position id ofr key in dict
    """
    if not isinstance(plate, TCA.Core.Plate):
        raise TypeError("\033[0;31m[ERROR]\033[0m Take a Plate object in inpout")
    else:
        data_dict = plate.get_all_raw_data()

        def get_number_cell_by_well(array):
            """
            Get Number of occurence by well
            :param array: is a replicat dataframe
            :return:
            """
            try:
                groupbydata = array.groupby('Well')
                count = groupbydata.Well.count()
                dictcount = count.to_dict()
                return dictcount
            except Exception as e:
                print("\033[0;31m[ERROR]\033[0m", e)

        dictmeanbyrep = {}
        try:
            for k, v in data_dict.items():
                cellcount = get_number_cell_by_well(v)
                for key in cellcount.keys():
                    try:
                        dictmeanbyrep.setdefault(key, []).append(cellcount[key])
                    except KeyError:
                        pass
            sdvalue = {}
            for key, value in dictmeanbyrep.items():
                sdvalue[key] = np.std(value)
            meancountlist = [(i, sum(v) / len(v)) for i, v in dictmeanbyrep.items()]
            meancount = dict(meancountlist)  # # convert to dict

            if verbose:
                mean = np.zeros(plate.PlateMap.platemap.shape)
                sd = np.zeros(plate.PlateMap.platemap.shape)

                for k, v in meancount.items():
                    well = TCA.Utils.WellFormat.get_opposite_well_format(k)
                    mean[well[0]][well[1]] = v

                for k, v in sdvalue.items():
                    well = TCA.Utils.WellFormat.get_opposite_well_format(k)
                    sd[well[0]][well[1]] = v

                print("Mean of number of Cells by well : ")
                print(mean)
                print("Standart deviation of number of Cells by Well : ")
                print(sd)

            return meancount, sdvalue
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m", e)
