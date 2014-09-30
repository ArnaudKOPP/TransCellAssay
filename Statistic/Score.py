__author__ = 'Arnaud KOPP'
"""
Score defined method for compute some score on data
"""


import Statistic.Result
import TCA
import numpy as np

def getPercentPosCell(rep1, rep2=None, rep3=None):
    '''
    get % of Cell over threshold
    :param rep1:
    :param rep2:
    :param rep3:
    :return:
    '''
    try:
        return 0
    except Exception as e:
        print(e)


def getMeanCount(dataDict):
    '''
    get mean of number of cell per well accross replicat
    :param dataDict : Give a dict that contains data frame value from replicat
    :return: return a dict that contain mean value for well
    '''
    def getNumberInDict(InputArray):
        '''
        Get Number of occurence by well
        :param Input: is a replicat
        :return:
        '''
        try:
            array = InputArray
            tmp = array.groupby('Well')
            count = tmp.Well.count()
            dictCount = count.to_dict()
            return dictCount
        except Exception as e:
            print(e)


    dictMeanByRep = {}
    try:
        for k, v in dataDict.items():
            CellCount = getNumberInDict(v)
            for key in CellCount.keys():
                try:
                    dictMeanByRep.setdefault(key, []).append(CellCount[key])
                except KeyError:
                    pass
        SDValue = getSDMeanCount(dictMeanByRep)
        MeanCount = [(i, sum(v)//len(v)) for i, v in dictMeanByRep.items()]
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


def getToxicity(rep1, rep2=None, rep3=None):
    '''
    determine a toxicity index
    :param rep1:
    :param rep2:
    :param rep3:
    :return:
    '''
    try:
        return 0
    except Exception as e:
        print(e)


def getInfection(rep1, rep2=None, rep3=None):
    '''
    determine a infection index
    :param rep1:
    :param rep2:
    :param rep3:
    :return:
    '''
    try:
        return 0
    except Exception as e:
        print(e)


def getViability(rep1, rep2=None, rep3=None):
    '''
    get Viability
    :param rep1:
    :param rep2:
    :param rep3:
    :return:
    '''
    try:
        return 0
    except Exception as e:
        print(e)


def getMean(feat, rep1, rep2=None, rep3=None):
    '''
    get Mean of interested value
    :param rep1:
    :param rep2:
    :param rep3:
    :param feat:
    :return:
    '''
    try:
        return 0
    except Exception as e:
        print(e)


def getMedian(feat, rep1, rep2=None, rep3=None):
    '''
    get median of interested value
    :param rep1:
    :param rep2:
    :param rep3:
    :param feat:
    :return:
    '''
    try:
        return 0
    except Exception as e:
        print(e)


def getMad(feat, rep1, rep2=None, rep3=None):
    '''
    get MAD of interested value
    :param rep1:
    :param rep2:
    :param rep3:
    :param feat:
    :return:
    '''
    try:
        return 0
    except Exception as e:
        print(e)


def getSSMD(feat, rep1, rep2=None, rep3=None):
    '''
    performed SSMD
    :param rep1:
    :param rep2:
    :param rep3:
    :param feat:
    :return:
    '''
    try:
        return 0
    except Exception as e:
        print(e)


def getSSMDr(feat, rep1, rep2=None, rep3=None):
    '''
    perfored SSMDr
    :param rep1:
    :param rep2:
    :param rep3:
    :param feat:
    :return:
    '''
    try:
        return 0
    except Exception as e:
        print(e)


def getPairedSSMD(feat, rep1=None, rep2=None, rep3=None):
    '''
    performed paired ssmd
    :param feat:
    :param rep1:
    :param rep2:
    :param rep3:
    :return:
    '''
    try:
        return 0
    except Exception as e:
        print(e)


def getPairedSSMDr(feat, rep1=None, rep2=None, rep3=None):
    '''
    performed paired SSMDr
    :param feat:
    :param rep1:
    :param rep2:
    :param rep3:
    :return:
    '''
    try:
        return 0
    except Exception as e:
        print(e)


def PairedTStat(feat, rep1=None, rep2=None, rep3=None):
    '''
    performed paired t statistic
    :param feat:
    :param rep1:
    :param rep2:
    :param rep3:
    :return:
    '''
    try:
        return 0
    except Exception as e:
        print(e)


def computePlateScore(Plate, feature):
    '''
    Compute all score/carac implemented before, for plate
    :param Plate: Plate object
    :return: return a result object
    '''
    platesetup = Plate.getPlateSetup()
    size = platesetup.getSize()
    result = Statistic.Result((size[0] * size[1]))
    try:
        assert isinstance(Plate, TCA.Plate)
        data = Plate.getAllData()
        meanCount, sdvalue = getMeanCount(data)
        print(meanCount, sdvalue)
        return result
    except Exception as e:
        print(e)