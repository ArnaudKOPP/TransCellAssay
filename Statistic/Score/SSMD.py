__author__ = 'Arnaud KOPP'
'''
Function that performed paired/unpaired SSMD and for plate without replicat

SSMD is the mean of differences divided bu the standard deviation of the differences between an siRNA and a negative
reference. In other words, SSMD is the average fold change (on the log scale) penalized by the variability of fold
change (on the log scsale).

In a screen without replicats, we cannot directly calculate the variability of each siRNA. Thus, like z-score, we have
to assume that each siRNA has the same variability as a negative reference and then calculate the variability based
on the negative reference and/or all investiged siRNAs. On the basis of this assumption, we can calculate SSMD using
method-of-moment(MM) method or the uniformy minimal variance unbiased estimate(UMVUE) method. The use of rebust version
is highly recommended.

In a screen with replicats:
For the paired case, a measured value for an siRNA is paired with a median value of a negative reference in the same
plate. The mean and variability of the difference of all these pairs accross all plates are used to calculate SSMD.
For the unpaired case, all the measured value of an siRNA are formed as a group and all the measured value of a negative
reference in the whole screen are formed as another group. The means and variability of these two separate groups are
used to calculate the ssmd.
'''
import ScreenPlateReplicatPS
import numpy as np
import scipy.special
from Statistic.Stat import mad


def ssmd_score(plate, cNeg, paired=True, robust_version=True, data='median', method='UMVUE', variance='unequal',
               verbose=False):
    '''
    Performed SSMD on plate object
        unpaired is for plate with replicat without great variance between them
        paired is for plate with replicat with great variance between them
    :param plate: Plate Object to analyze
    :param cNeg: negative control reference
    :param paired: paired or unpaired statistic
    :param robust_version: use robust version or not
    :param data: median or mean data to use
    :param method: which method to use MM or UMVUE
    :param variance: unequal or equal
    :param verbose: be verbose or not
    :return:
    '''
    try:
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            # if no neg was provided raise AttributeError
            if cNeg is None:
                raise AttributeError('Must provided negative control')
            if len(plate) > 1:
                print('SSMD optimize for plate with replicat')
                if not paired:
                    print('Using : _getUnpairedSSMD')
                    _getUnpairedSSMD(plate, cNeg, variance=variance, data=data, verbose=verbose)
                else:
                    if robust_version:
                        print('Using : _getPairedSSMDr')
                        _getPairedSSMDr(plate, cNeg, data=data, method=method, verbose=verbose)
                    else:
                        print('Using : _getPairedSSMD')
                        _getPairedSSMD(plate, cNeg, data=data, method=method, verbose=verbose)
            else:
                print('SSMD optimize for plate without replicat')
                if robust_version:
                    print('Using : _getWithoutReplicatSSMDr')
                    _getWithoutReplicatSSMDr(plate, cNeg, data=data, method=method, verbose=verbose)
                else:
                    print('Using : _getWithoutReplicatSSMD')
                    _getWithoutReplicatSSMD(plate, cNeg, data=data, method=method, verbose=verbose)
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _getUnpairedSSMD(plate, cNeg, variance='unequal', data='median', verbose=False):
    '''
    performed unpaired SSMD for plate with replicat
    :param plate: Plate Object to analyze
    :param cNeg: negative control reference
    :param variance: unequal or equal
    :param data: median or mean data to use
    :param verbose: be verbose or not
    :return:
    '''
    try:
        # if no neg was provided raise AttributeError
        if cNeg is None:
            raise AttributeError('Must provided negative control')
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            SSMD = np.zeros(plate.PlateSetup.platesetup.shape)
            nb_rep = len(plate.replicat)
            rep_value = []
            neg_value = []
            neg_pos = plate.PlateSetup.getGenePos(cNeg)

            # search neg control value
            for i in range(SSMD.shape[0]):
                for j in range(SSMD.shape[1]):
                    for key, value in plate.replicat.items():
                        well_value = 0
                        try:
                            if data == "median":
                                well_value = value.SpatNormDataMedian[i][j]
                            elif data == "mean":
                                well_value = value.SpatNormDataMean[i][j]
                            else:
                                raise AttributeError('Data type must be mean or median')
                        except Exception:
                            raise Exception("Launch SystematicErrorCorrection before")
                        # check if neg value
                        for neg_i in neg_pos:
                            if neg_i[0] == i and neg_i[1] == j:
                                neg_value.append(well_value)
            nb_neg_wells = len(neg_value)
            mean_neg = np.mean(neg_value)
            var_neg = np.var(neg_value)

            k = 2 * (scipy.special.gamma(
                ((len(neg_value) - 1) / 2) / scipy.special.gamma((len(neg_value) - 2) / 2))) ** 2
            # search rep value for ith well
            for i in range(SSMD.shape[0]):
                for j in range(SSMD.shape[1]):
                    well_value = 0
                    for key, value in plate.replicat.items():
                        try:
                            if data == "median":
                                well_value = value.SpatNormDataMedian[i][j]
                            elif data == "mean":
                                well_value = value.SpatNormDataMean[i][j]
                            else:
                                raise AttributeError('Data type must be mean or median')
                        except Exception:
                            raise Exception("Launch SystematicErrorCorrection before")
                        rep_value.append(well_value)
                    mean_rep = np.mean(rep_value)
                    var_rep = np.var(rep_value)

                    # # performed unpaired t-test
                    if variance == 'unequal':
                        SSMD[i][j] = (mean_rep - mean_neg) / np.sqrt(var_rep + var_neg)
                    elif variance == 'equal':
                        SSMD[i][j] = (mean_rep - mean_neg) / np.sqrt(
                            (2 / k) * ((nb_rep - 1) * var_rep + (nb_neg_wells - 1) * var_neg))
                    else:
                        raise AttributeError('variance attribut must be unequal or equal.')
            if verbose:
                print("Unpaired SSMD :")
                print("Data type : ", data)
                print("variance parameter : ", variance)
                print("SSMD score :")
                print(SSMD)
                print("")
            return SSMD
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _getPairedSSMD(plate, cNeg, data='median', method='UMVUE', verbose=False):
    '''
    performed paired ssmd for plate with replicat
    :param plate: Plate Object to analyze
    :param cNeg: negative control reference
    :param data: median or mean data to use
    :param method: which method to use MM or UMVUE
    :param verbose: be verbose or not
    :return:
    '''
    try:
        # if no neg was provided raise AttributeError
        if cNeg is None:
            raise AttributeError('Must provided negative control')
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            SSMD = np.zeros(plate.PlateSetup.platesetup.shape)
            neg_value = []
            neg_pos = plate.PlateSetup.getGenePos(cNeg)

            # search neg control value
            def _search_neg_data(replicat, neg_pos, data):
                try:
                    for i in range(SSMD.shape[0]):
                        for j in range(SSMD.shape[1]):
                            well_value = 0
                            try:
                                if data == "median":
                                    well_value = replicat.SpatNormDataMedian[i][j]
                                elif data == "mean":
                                    well_value = replicat.SpatNormDataMean[i][j]
                                else:
                                    raise AttributeError('Data type must be mean or median')
                            except Exception:
                                raise Exception("Launch SystematicErrorCorrection before")
                            # check if neg value
                            for neg_i in neg_pos:
                                if neg_i[0] == i and neg_i[1] == j:
                                    neg_value.append(well_value)
                    return np.median(neg_value)
                except Exception as e:
                    print(e)

            x = (scipy.special.gamma((len(plate.replicat) - 1) / 2) / scipy.special.gamma(
                (len(plate.replicat) - 2) / 2)) * np.sqrt(2 / (len(plate.replicat) - 1))

            try:
                for i in range(SSMD.shape[0]):
                    for j in range(SSMD.shape[1]):
                        well_value = []
                        for key, value in plate.replicat.items():

                            neg_median = _search_neg_data(value, neg_pos, data)

                            if data == 'median':
                                well_value.append(value.SpatNormDataMedian[i][j] - neg_median)
                            elif data == 'mean':
                                well_value.append(value.SpatNormDataMean[i][j] - neg_median)
                            else:
                                raise AttributeError('Median or Mean data only')
                        if method == 'UMVUE':
                            SSMD[i][j] = x * (np.mean(well_value) / np.std(well_value))
                        elif method == 'MM':
                            SSMD[i][j] = np.mean(well_value) / np.std(well_value)
                        else:
                            raise AttributeError('Method must me UMVUE or MM')
                if verbose:
                    print("Paired SSMD :")
                    print("Data type : ", data)
                    print("method parameter : ", method)
                    print("SSMD score :")
                    print(SSMD)
                    print("")
            except Exception as e:
                print(e)
            return SSMD
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _getPairedSSMDr(plate, cNeg, data='median', method='UMVUE', verbose=False):
    '''
    performed paired SSMDr for plate with replicat
    :param plate: Plate Object to analyze
    :param cNeg: negative control reference
    :param data: median or mean data to use
    :param method: which method to use MM or UMVUE
    :param verbose: be verbose or not
    :return:
    '''
    try:
        # if no neg was provided raise AttributeError
        if cNeg is None:
            raise AttributeError('Must provided negative control')
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            SSMDr = np.zeros(plate.PlateSetup.platesetup.shape)

            neg_value = []
            neg_pos = plate.PlateSetup.getGenePos(cNeg)

            # search neg control value
            def _search_neg_data(replicat, neg_pos, data):
                try:
                    for i in range(SSMDr.shape[0]):
                        for j in range(SSMDr.shape[1]):
                            well_value = 0
                            try:
                                if data == "median":
                                    well_value = replicat.SpatNormDataMedian[i][j]
                                elif data == "mean":
                                    well_value = replicat.SpatNormDataMean[i][j]
                                else:
                                    raise AttributeError('Data type must be mean or median')
                            except Exception:
                                raise Exception("Launch SystematicErrorCorrection before")
                            # check if neg value
                            for neg_i in neg_pos:
                                if neg_i[0] == i and neg_i[1] == j:
                                    neg_value.append(well_value)
                    return np.median(neg_value)
                except Exception as e:
                    print(e)


            x = (scipy.special.gamma((len(plate.replicat) - 1) / 2) / scipy.special.gamma(
                (len(plate.replicat) - 2) / 2)) * np.sqrt(2 / (len(plate.replicat) - 1))

            try:
                for i in range(SSMDr.shape[0]):
                    for j in range(SSMDr.shape[1]):
                        well_value = []
                        for key, value in plate.replicat.items():

                            neg_median = _search_neg_data(value, neg_pos, data)

                            if data == 'median':
                                well_value.append(value.SpatNormDataMedian[i][j] - neg_median)
                            elif data == 'mean':
                                well_value.append(value.SpatNormDataMean[i][j] - neg_median)
                            else:
                                raise AttributeError('Median or Mean data only')
                        if method == 'UMVUE':
                            SSMDr[i][j] = x * (np.median(well_value) / mad(well_value))
                        elif method == 'MM':
                            SSMDr[i][j] = np.median(well_value) / mad(well_value)
                        else:
                            raise AttributeError('Method must me UMVUE or MM')
                if verbose:
                    print("Paired SSMDr :")
                    print("Data type : ", data)
                    print("method parameter : ", method)
                    print("SSMDr score :")
                    print(SSMDr)
                    print("")
            except Exception as e:
                print(e)
            return SSMDr
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _getWithoutReplicatSSMD(plate, cNeg, data='median', method='UMVUE', verbose=False):
    '''
    performed unpaired SSMD for plate without replicat
    take data from plate and spatial norm data
    :param plate: Plate Object to analyze
    :param cNeg: negative control reference
    :param data: median or mean data to use
    :param method: which method to use MM or UMVUE
    :param verbose: be verbose or not
    :return:
    '''
    try:
        # if no neg was provided raise AttributeError
        if cNeg is None:
            raise AttributeError('Must provided negative control')
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            ps = plate.PlateSetup
            ssmd = np.zeros(ps.shape)
            neg_well = ps.getGenePos(cNeg)
            neg_data = []
            try:
                if data == 'median':
                    data = plate.SpatNormDataMedian
                elif data == 'mean':
                    data = plate.SpatNormDataMean
                else:
                    raise AttributeError('Median or Mean data only')
            except Exception:
                raise Exception("Launch SystematicErrorCorrection before")
            # grab all neg data
            for neg_pos in neg_well:
                neg_data.append(data[neg_pos[0]][neg_pos[1]])
            # check if len is sufficient
            if len(neg_data) < 2:
                raise ValueError('Insuficient negative data')

            try:
                if method == 'MM':
                    ssmd = (data - np.mean(neg_data)) / (np.sqrt(2) * np.std(neg_data))
                elif method == 'UMVUE':
                    k = 2 * (scipy.special.gamma(
                        ((len(neg_data) - 1) / 2) / scipy.special.gamma((len(neg_data) - 2) / 2))) ** 2
                    ssmd = (data - np.mean(neg_data)) / (np.sqrt((2 / k) * (len(neg_data))) * np.std(neg_data))
                else:
                    raise AttributeError('Method must be MM or UMVUE')
            except Exception as e:
                print(e)
            if verbose:
                print('SSMD without replicat')
                print("Data type : ", data)
                print("method parameter : ", method)
                print("SSMD score :")
                print(ssmd)
                print("")
            return ssmd
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _getWithoutReplicatSSMDr(plate, cNeg, data='median', method='UMVUE', verbose=False):
    '''
    perfored unpaired SSMDr for plate without replicat
    :param plate: Plate Object to analyze
    :param cNeg: negative control reference
    :param data: median or mean data to use
    :param method: which method to use MM or UMVUE
    :param verbose: be verbose or not
    :return:
    '''
    try:
        # if no neg was provided raise AttributeError
        if cNeg is None:
            raise AttributeError('Must provided negative control')
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            ps = plate.PlateSetup
            ssmdr = np.zeros(ps.shape)
            neg_well = ps.getGenePos(cNeg)
            neg_data = []
            try:
                if data == 'median':
                    data = plate.SpatNormDataMedian
                elif data == 'mean':
                    data = plate.SpatNormDataMean
                else:
                    raise AttributeError('Median or Mean data only')
            except Exception:
                raise Exception("Launch SystematicErrorCorrection before")
            # grab all neg data
            for neg_pos in neg_well:
                neg_data.append(data[neg_pos[0]][neg_pos[1]])
            # check if len is sufficient
            if len(neg_data) < 2:
                raise ValueError('Insuficient negative data')

            try:
                if method == 'MM':
                    ssmdr = (data - np.median(neg_data)) / (np.sqrt(2) * mad(neg_data))
                elif method == 'UMVUE':
                    k = 2 * (scipy.special.gamma(
                        ((len(neg_data) - 1) / 2) / scipy.special.gamma((len(neg_data) - 2) / 2))) ** 2
                    ssmdr = (data - np.median(neg_data)) / (np.sqrt((2 / k) * (len(neg_data))) * mad(neg_data))
                else:
                    raise AttributeError('Method must be MM or UMVUE')
            except Exception as e:
                print(e)
            if verbose:
                print('SSMDr without replicat')
                print("Data type : ", data)
                print("method parameter : ", method)
                print("SSMD score :")
                print(ssmdr)
                print("")
            return ssmdr
        else:
            raise TypeError
    except Exception as e:
        print(e)