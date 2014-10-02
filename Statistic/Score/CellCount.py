__author__ = 'Arnaud KOPP'

import numpy as np

def getMeanSDCellCount(dataDict):
    '''
    get mean of number of cell per well accross replicat
    :param dataDict : Give a dict that contains dataframe value from replicat
    :return: return a dict that contain mean value for well, with well position id ofr key in dict
    '''

    def getNumberCellByWell(InputArray):
        '''
        Get Number of occurence by well
        :param Input: is a replicat dataframe
        :return:
        '''
        try:
            tmp = InputArray.groupby('Well')
            count = tmp.Well.count()
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
        SDValue = getSDMeanCount(dictMeanByRep)
        MeanCountList = [(i, sum(v) // len(v)) for i, v in dictMeanByRep.items()]
        MeanCount = dict(MeanCountList)  # # convert to dict
        return MeanCount, SDValue
    except Exception as e:
        print(e)


def getSDMeanCount(dictmeanbyrep):
    '''
    get Standart deviation of cell per well accross replicat
    Need a least two replicat
    :param dictmeanbyrep: Give a dict that contain number of cell by well for all replicat
    :return: retrun a dict that contain standart deviation of nb cell for well
    '''
    dictsdbyrep = {}
    try:
        for key, value in dictmeanbyrep.items():
            dictsdbyrep[key] = np.std(value)
        return dictsdbyrep
    except Exception as e:
        print(e)