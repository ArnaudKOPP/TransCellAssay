__author__ = 'Arnaud KOPP'
'''
Function that performed paired/unpaired SSMD and for plate without replicat
'''
import ScreenPlateReplicatPS
import numpy as np
import scipy.special
from Statistic.Stat import mad


def ssmd_score(plate, cNeg, paired=True, robust_version=True, data='median', method='MM', verbose=False):
    '''
    Performed SSMD on plate object
    unpaired is for plate with replicat without great variance between them
    paired is for plate with replicat with great variance between them
    :param Plate:
    :return:
    '''
    try:
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            if len(plate) > 1:
                print('SSMD optimize for plate with replicat')
            else:
                print('SSMD optimize for plate without replicat')
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _getUnpairedSSMD(plate, cNeg, data='median', verbose=False):
    '''
    performed unpaired SSMD for plate with replicat
    :return:
    '''
    try:
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            if not cNeg is None:
                return 0
            else:
                raise AttributeError
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _getUnpairedSSMDr(plate, cNeg, data='median', verbose=False):
    '''
    perfored unpaired SSMDr for plate with replicat
    :return:
    '''
    try:
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            if not cNeg is None:
                return 0
            else:
                raise AttributeError
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _getPairedSSMD(plate, data='median', method='UMVUE', verbose=False):
    '''
    performed paired ssmd for plate with replicat
    :return:
    '''
    try:
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            SSMD = np.zeros(plate.PlateSetup.platesetup.shape)
            try:
                if data == 'median':
                    for i in range(SSMD.shape[0]):
                        for j in range(SSMD.shape[1]):
                            well_value = []
                            for key, value in plate.replicat.items():
                                well_value.append(value.SpatNormDataMedian[i][j])
                            if method == 'UMVUE':
                                SSMD[i][j] = (scipy.special.gamma((len(plate.replicat) - 1) / 2) / scipy.special.gamma(
                                    (len(plate.replicat) - 2) / 2)) * np.sqrt(2 / (len(plate.replicat) - 1)) * \
                                             (np.mean(well_value) / np.std(well_value))
                            else:
                                SSMD[i][j] = np.mean(well_value) / np.std(well_value)
                else:
                    for i in range(SSMD.shape[0]):
                        for j in range(SSMD.shape[1]):
                            well_value = []
                            for key, value in plate.replicat.items():
                                well_value.append(value.SpatNormDataMedian[i][j])
                                if method == 'UMVUE':
                                    SSMD[i][j] = (scipy.special.gamma(
                                        (len(plate.replicat) - 1) / 2) / scipy.special.gamma(
                                        (len(plate.replicat) - 2) / 2)) * np.sqrt(2 / (len(plate.replicat) - 1)) * \
                                                 (np.mean(well_value) / np.std(well_value))
                                else:
                                    SSMD[i][j] = np.mean(well_value) / np.std(well_value)
                if verbose:
                    print('SSMD without replicat, with method : ', method, ' on ', data, ' data')
                    print(SSMD)
            except Exception as e:
                print(e)
            return SSMD
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _getPairedSSMDr(plate, data='median', method='UMVUE', verbose=False):
    '''
    performed paired SSMDr for plate with replicat
    :return:
    '''
    try:
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            SSMDr = np.zeros(plate.PlateSetup.platesetup.shape)
            try:
                if data == 'median':
                    for i in range(SSMDr.shape[0]):
                        for j in range(SSMDr.shape[1]):
                            well_value = []
                            for key, value in plate.replicat.items():
                                well_value.append(value.SpatNormDataMedian[i][j])
                            if method == 'UMVUE':
                                SSMDr[i][j] = (scipy.special.gamma((len(plate.replicat) - 1) / 2) / scipy.special.gamma(
                                    (len(plate.replicat) - 2) / 2)) * np.sqrt(2 / (len(plate.replicat) - 1)) * \
                                              (np.median(well_value) / mad(well_value))
                            else:
                                SSMDr[i][j] = np.median(well_value) / mad(well_value)
                else:
                    for i in range(SSMDr.shape[0]):
                        for j in range(SSMDr.shape[1]):
                            well_value = []
                            for key, value in plate.replicat.items():
                                well_value.append(value.SpatNormDataMedian[i][j])
                            if method == 'UMVUE':
                                SSMDr[i][j] = (scipy.special.gamma((len(plate.replicat) - 1) / 2) / scipy.special.gamma(
                                    (len(plate.replicat) - 2) / 2)) * np.sqrt(2 / (len(plate.replicat) - 1)) * \
                                              (np.median(well_value) / mad(well_value))
                            else:
                                SSMDr[i][j] = np.mean(well_value) / np.std(well_value)
                if verbose:
                    print('SSMDr without replicat, with method : ', method, ' on ', data, ' data')
                    print(SSMDr)
            except Exception as e:
                print(e)
            return SSMDr
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _getSSMDWithoutReplicat(plate, cNeg, data='median', method='UMVUE', verbose=False):
    '''
    performed unpaired SSMD for plate without replicat
    take data from plate and spatial norm data
    :return:
    '''
    try:
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            # if no neg was provided raise AttributeError
            if not cNeg is None:
                ps = plate.PlateSetup
                neg_well = ps.getGenePos(cNeg)
                neg_data = []
                try:
                    if data == 'median':
                        data = plate.SpatNormDataMedian
                    else:
                        data = plate.SpatNormDataMean
                except Exception as e:
                    print("Launch SystematicErrorCorrection before")
                    print(e)
                for neg_pos in neg_well:
                    neg_data.append(data[neg_pos[0]][neg_pos[1]])
                if len(neg_data) < 2:
                    print('Insuficient negative data')
                    raise ValueError
                if method == 'MM':
                    ssmd = (data - np.mean(neg_data)) / (np.sqrt(2) * np.std(neg_data))
                    if verbose:
                        print('SSMD without replicat, with method : ', method, ' on ', data, ' data')
                        print(ssmd)
                    return ssmd
                elif method == 'UMVUE':
                    k = 2 * (scipy.special.gamma(
                        ((len(neg_data) - 1) / 2) / scipy.special.gamma((len(neg_data) - 2) / 2))) ** 2
                    ssmd = (data - np.mean(neg_data)) / (np.sqrt((2 / k) * (len(neg_data))) * np.std(neg_data))
                    if verbose:
                        print('SSMD without replicat, with method : ', method, ' on ', data, ' data')
                        print(ssmd)
                    return ssmd
                else:
                    raise AttributeError
            else:
                raise AttributeError
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _getSSMDrWithoutReplicat(plate, cNeg, data='median', method='UMVUE', verbose=False):
    '''
    perfored unpaired SSMDr for plate without replicat
    :return:
    '''
    try:
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            # if no neg was provided raise AttributeError
            if not cNeg is None:
                ps = plate.PlateSetup
                neg_well = ps.getGenePos(cNeg)
                neg_data = []
                try:
                    if data == 'median':
                        data = plate.SpatNormDataMedian
                    else:
                        data = plate.SpatNormDataMean
                except Exception as e:
                    print("Launch SystematicErrorCorrection before")
                    print(e)
                for neg_pos in neg_well:
                    neg_data.append(data[neg_pos[0]][neg_pos[1]])
                if len(neg_data) < 2:
                    print('Insuficient negative data')
                    raise ValueError
                if method == 'MM':
                    ssmdr = (data - np.median(neg_data)) / (np.sqrt(2) * mad(neg_data))
                    if verbose:
                        print('SSMDr without replicat, with method : ', method, ' on ', data, ' data')
                        print(ssmdr)
                    return ssmdr
                elif method == 'UMVUE':
                    k = 2 * (scipy.special.gamma(
                        ((len(neg_data) - 1) / 2) / scipy.special.gamma((len(neg_data) - 2) / 2))) ** 2
                    ssmdr = (data - np.median(neg_data)) / (np.sqrt((2 / k) * (len(neg_data))) * mad(neg_data))
                    if verbose:
                        print('SSMDr without replicat, with method : ', method, ' on ', data, ' data')
                        print(ssmdr)
                    return ssmdr
                else:
                    raise AttributeError
            else:
                raise AttributeError
        else:
            raise TypeError
    except Exception as e:
        print(e)