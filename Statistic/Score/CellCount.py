__author__ = 'Arnaud KOPP'
import ScreenPlateReplicatPS
import numpy as np


def getMeanSDCellCount(plate):
    """
    get mean of number of cell per well accross replicat
    :param plate : Give a TCA.Plate object
    :return: return a dict that contain mean value for well, with well position id ofr key in dict
    """
    if not isinstance(plate, ScreenPlateReplicatPS.Plate):
        raise TypeError
    else:
        dataDict = plate.getAllData()

        def getNumberCellByWell(InputArray):
            '''
            Get Number of occurence by well
            :param Input: is a replicat dataframe
            :return:
            '''
            try:
                groupbydata = InputArray.groupby('Well')
                count = groupbydata.Well.count()
                dictCount = count.to_dict()
                return dictCount
            except Exception as e:
                print(e)


        dictMeanByRep = {}
        try:
            for k, v in dataDict.items():
                CellCount = getNumberCellByWell(v)
                for key in CellCount.keys():
                    try:
                        dictMeanByRep.setdefault(key, []).append(CellCount[key])
                    except KeyError:
                        pass
            SDValue = {}
            for key, value in dictMeanByRep.items():
                SDValue[key] = np.std(value)
            MeanCountList = [(i, sum(v) / len(v)) for i, v in dictMeanByRep.items()]
            MeanCount = dict(MeanCountList)  # # convert to dict
            return MeanCount, SDValue
        except Exception as e:
            print("\033[0;31m[ERROR]\033[0m")
            print(e)
