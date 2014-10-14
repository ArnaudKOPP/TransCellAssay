__author__ = 'Arnaud KOPP'
"""
PlateNorm define method for normalizing a plate, replicat are quantile norm for giving them same distribution style
"""
import TCA
import numpy as np


def PlateNorm(plate, feature):
    """
    Normalized a Plate object by quantile normalization
    quantile normalization is a technique for making two distributions identical in statistical properties

    BIG DIRTY WORK HERE

    :param anarray:
    :return: return array
    """
    if isinstance(plate, TCA.Plate):
        if plate.getNumberReplicat() >= 2:
            data = {}
            WellList = None
            # # iterate on replicat to get well list
            for key, value in plate.replicat.items():
                if WellList is None:
                    WellList = value.Data.Well.unique()
            ## iterate on well
            for well in WellList:
                pot = None
                for key, value in plate.replicat.items():
                    data[key] = value.getDataByWells(feature, well)
                    pot += data[key]
                for key, value in plate.replicat.items():
                    A = value.Data[feature][value.Data['Well'] == well]
                    AA = np.float64(np.zeros_like(A))  # result array creation
                    I = np.argsort(A, axis=0)
                    AA[I, np.arange(A.shape[1])] = np.float64(np.mean(pot)[:, np.newaxis])
                    value.Data[feature][value.Data['Well'] == well] = AA
        else:
            print('No needs, only one replicat')
            return 0
    else:
        print('Take a Plate Object')
        raise TypeError


def quantile_normalization(anarray):
    """
    anarray with samples in the columns and probes across the rows
    :param anarray:
    :return: return array
    """
    try:
        anarray.dtype = np.float64
        A = anarray
        AA = np.float64(np.zeros_like(A))  # result array creation
        I = np.argsort(A, axis=0)  # sort array
        AA[I, np.arange(A.shape[1])] = np.float64(np.mean(A[I, np.arange(A.shape[1])], axis=1)[:, np.newaxis])
        return AA
    except Exception as e:
        print(e)


