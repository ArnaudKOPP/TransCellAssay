__author__ = 'Arnaud KOPP'
"""
Score defined method for compute some score on data
"""
# #Defined method for compute score and data of plate
# #
# #

import Math.Result
import TCA


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


def getMeanCount(rep1, rep2=None, rep3=None):
    '''
    get mean of number of cell per well accross replicat
    :param rep1:
    :param rep2:
    :param rep3:
    :return:
    '''
    try:
        array = rep1.getData()
        tmp = array.groupby('Well')
        count = tmp.Well.count()
        return 0
    except Exception as e:
        print(e)


def getSDMeanCount(rep1, rep2, rep3=None):
    '''
    get Standart deviation of cell per well accross replicat
    Need a least two replicat
    :param rep1:
    :param rep2:
    :param rep3:
    :return:
    '''
    try:
        return 0
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
    result = Math.Result.Result()
    try:
        assert isinstance(Plate, TCA.Plate)
        allrep = Plate.getAllReplicat()
        for rep in allrep:
            data = rep.getDataByFeatures([feature])
        return result
    except Exception as e:
        print(e)