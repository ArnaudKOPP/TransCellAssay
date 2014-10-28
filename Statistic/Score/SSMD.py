"""
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
"""

import ScreenPlateReplicatPS
import numpy as np
import scipy.special
from Statistic.Stat import mad

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def ssmd_score(plate, cNeg, paired=True, robust_version=True, method='UMVUE', variance='unequal', SECData=True,
               inplate_data=False, verbose=False):
    """
    Performed SSMD on plate object
        unpaired is for plate with replicat without great variance between them
        paired is for plate with replicat with great variance between them
    :param plate: Plate Object to analyze
    :param cNeg: negative control reference
    :param paired: paired or unpaired statistic
    :param robust_version: use robust version or not
    :param method: which method to use MM or UMVUE
    :param variance: unequal or equal
    :param SECData: use data with Systematic Error Corrected
    :param inplate_data: compute SSMD on plate.Data, for plate without replicat in preference
    :param verbose: be verbose or not
    :return: Corrected data
    """
    try:
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            # if no neg was provided raise AttributeError
            if cNeg is None:
                raise AttributeError('Must provided negative control')
            if len(plate) > 1 and not inplate_data:
                print('SSMD optimize for plate with replicat')
                if not paired:
                    if robust_version:
                        print('Using : _getUnpairedSSMDr')
                        score = _UnpairedSSMDr(plate, cNeg, variance=variance, SECData=SECData,
                                               verbose=verbose)
                    else:
                        print('Using : _getUnpairedSSMD')
                        score = _UnpairedSSMD(plate, cNeg, variance=variance, SECData=SECData,
                                              verbose=verbose)
                else:
                    if robust_version:
                        print('Using : _getPairedSSMDr')
                        score = _PairedSSMDr(plate, cNeg, method=method, SECData=SECData, verbose=verbose)
                    else:
                        print('Using : _getPairedSSMD')
                        score = _PairedSSMD(plate, cNeg, method=method, SECData=SECData, verbose=verbose)
            else:
                print('SSMD optimize for plate without replicat')
                if robust_version:
                    print('Using : _SSMDr')
                    score = _SSMDr(plate, cNeg, method=method, SECData=SECData, verbose=verbose)
                else:
                    print('Using : _SSMD')
                    score = _SSMD(plate, cNeg, method=method, SECData=SECData, verbose=verbose)
            return score
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _UnpairedSSMD(plate, cNeg, variance='unequal', SECData=True, verbose=False):
    """
    performed unpaired SSMD for plate with replicat
    :param plate: Plate Object to analyze
    :param cNeg: negative control reference
    :param variance: unequal or equal
    :param SECData: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return:score data
    """
    try:
        # if no neg was provided raise AttributeError
        if cNeg is None:
            raise AttributeError('\033[0;31m[ERROR]\033[0m  Must provided negative control')
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            SSMD = np.zeros(plate.PlateSetup.platesetup.shape)

            # # replace 0 with NaN
            SSMD[SSMD == 0] = np.NaN

            nb_rep = len(plate.replicat)
            rep_value = []
            neg_value = []
            neg_pos = plate.PlateSetup.getGenePos(cNeg)
            if not neg_pos:
                raise Exception
            # search neg control value
            for i in range(SSMD.shape[0]):
                for j in range(SSMD.shape[1]):
                    for key, value in plate.replicat.items():
                        well_value = 0
                        try:
                            if SECData:
                                well_value = value.SECData[i][j]
                            else:
                                well_value = value.Data[i][j]
                        except Exception:
                            raise Exception("\033[0;31m[ERROR]\033[0m  Your desired datatype are not available")
                        # check if neg value
                        for neg_i in neg_pos:
                            if neg_i[0] == i:
                                if neg_i[1] == j:
                                    neg_value.append(well_value)
            nb_neg_wells = len(neg_value)
            mean_neg = np.nanmean(neg_value)
            var_neg = np.nanvar(neg_value)

            k = 2 * (scipy.special.gamma(
                ((len(neg_value) - 1) / 2) / scipy.special.gamma((len(neg_value) - 2) / 2))) ** 2
            # search rep value for ith well
            for i in range(SSMD.shape[0]):
                for j in range(SSMD.shape[1]):
                    well_value = 0
                    for key, value in plate.replicat.items():
                        try:
                            if SECData:
                                well_value = value.SECData[i][j]
                            else:
                                well_value = value.Data[i][j]
                        except Exception:
                            raise Exception("\033[0;31m[ERROR]\033[0m  Your desired datatype are not available")
                        rep_value.append(well_value)
                    mean_rep = np.nanmean(rep_value)
                    var_rep = np.nanvar(rep_value)

                    # # performed unpaired t-test
                    if variance == 'unequal':
                        SSMD[i][j] = (mean_rep - mean_neg) / np.sqrt(var_rep + var_neg)
                    elif variance == 'equal':
                        SSMD[i][j] = (mean_rep - mean_neg) / np.sqrt(
                            (2 / k) * ((nb_rep - 1) * var_rep + (nb_neg_wells - 1) * var_neg))
                    else:
                        raise AttributeError('\033[0;31m[ERROR]\033[0m  variance attribut must be unequal or equal.')

            # # replace NaN with 0
            SSMD = np.nan_to_num(SSMD)

            if verbose:
                print("Unpaired SSMD :")
                print("Systematic Error Corrected Data : ", SECData)
                print("Data type : ", plate.DataType)
                print("variance parameter : ", variance)
                print("SSMD score :")
                print(SSMD)
                print("")
            return SSMD
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _UnpairedSSMDr(plate, cNeg, variance='unequal', SECData=True, verbose=False):
    """
    performed unpaired SSMDr for plate with replicat
    :param plate: Plate Object to analyze
    :param cNeg: negative control reference
    :param variance: unequal or equal
    :param SECData: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return:score data
    """
    try:
        # if no neg was provided raise AttributeError
        if cNeg is None:
            raise AttributeError('\033[0;31m[ERROR]\033[0m  Must provided negative control')
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            SSMD = np.zeros(plate.PlateSetup.platesetup.shape)

            # # replace 0 with NaN
            SSMD[SSMD == 0] = np.NaN

            nb_rep = len(plate.replicat)
            rep_value = []
            neg_value = []
            neg_pos = plate.PlateSetup.getGenePos(cNeg)
            if not neg_pos:
                raise Exception
            # search neg control value
            for i in range(SSMD.shape[0]):
                for j in range(SSMD.shape[1]):
                    for key, value in plate.replicat.items():
                        well_value = 0
                        try:
                            if SECData:
                                well_value = value.SECData[i][j]
                            else:
                                well_value = value.Data[i][j]
                        except Exception:
                            raise Exception("\033[0;31m[ERROR]\033[0m  Your desired datatype are not available")
                        # check if neg value
                        for neg_i in neg_pos:
                            if neg_i[0] == i:
                                if neg_i[1] == j:
                                    neg_value.append(well_value)
            nb_neg_wells = len(neg_value)
            median_neg = np.nanmedian(neg_value)
            var_neg = np.nanvar(neg_value)

            k = 2 * (scipy.special.gamma(
                ((len(neg_value) - 1) / 2) / scipy.special.gamma((len(neg_value) - 2) / 2))) ** 2
            # search rep value for ith well
            for i in range(SSMD.shape[0]):
                for j in range(SSMD.shape[1]):
                    well_value = 0
                    for key, value in plate.replicat.items():
                        try:
                            if SECData:
                                well_value = value.SECData[i][j]
                            else:
                                well_value = value.Data[i][j]
                        except Exception:
                            raise Exception("\033[0;31m[ERROR]\033[0m  Your desired datatype are not available")
                        rep_value.append(well_value)
                    median_rep = np.nanmedian(rep_value)
                    var_rep = np.nanvar(rep_value)

                    # # performed unpaired t-test
                    if variance == 'unequal':
                        SSMD[i][j] = (median_rep - median_neg) / np.sqrt(var_rep + var_neg)
                    elif variance == 'equal':
                        SSMD[i][j] = (median_rep - median_neg) / np.sqrt(
                            (2 / k) * ((nb_rep - 1) * var_rep + (nb_neg_wells - 1) * var_neg))
                    else:
                        raise AttributeError('\033[0;31m[ERROR]\033[0m  variance attribut must be unequal or equal.')

            # # replace NaN with 0
            SSMD = np.nan_to_num(SSMD)

            if verbose:
                print("Unpaired SSMDr :")
                print("Systematic Error Corrected Data : ", SECData)
                print("Data type : ", plate.DataType)
                print("variance parameter : ", variance)
                print("SSMD score :")
                print(SSMD)
                print("")
            return SSMD
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _PairedSSMD(plate, cNeg, method='UMVUE', SECData=True, verbose=False):
    """
    performed paired ssmd for plate with replicat
    :param plate: Plate Object to analyze
    :param cNeg: negative control reference
    :param method: which method to use MM or UMVUE
    :param SECData: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return:score data
    """
    try:
        # if no neg was provided raise AttributeError
        if cNeg is None:
            raise AttributeError('\033[0;31m[ERROR]\033[0m  Must provided negative control')
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            SSMD = np.zeros(plate.PlateSetup.platesetup.shape)

            # # replace 0 with NaN
            SSMD[SSMD == 0] = np.NaN

            neg_pos = plate.PlateSetup.getGenePos(cNeg)
            if not neg_pos:
                raise Exception

            # search neg control value
            def _search_neg_data(replicat, Neg_Pos):
                neg_value = []
                for i in range(SSMD.shape[0]):
                    for j in range(SSMD.shape[1]):
                        well_value = 0
                        try:
                            if SECData:
                                well_value = replicat.SECData[i][j]
                            else:
                                well_value = replicat.Data[i][j]
                        except Exception:
                            raise Exception("\033[0;31m[ERROR]\033[0m  Your desired datatype are not available")
                        # check if neg value
                        for neg_i in Neg_Pos:
                            if neg_i[0] == i:
                                if neg_i[1] == j:
                                    neg_value.append(well_value)
                return np.nanmedian(neg_value)

            x = (scipy.special.gamma((len(plate.replicat) - 1) / 2) / scipy.special.gamma(
                (len(plate.replicat) - 2) / 2)) * np.sqrt(2 / (len(plate.replicat) - 1))

            try:
                for i in range(SSMD.shape[0]):
                    for j in range(SSMD.shape[1]):
                        well_value = []
                        for key, value in plate.replicat.items():
                            neg_median = _search_neg_data(value, neg_pos)
                            if SECData:
                                well_value.append(value.SECData[i][j] - neg_median)
                            else:
                                well_value.append(value.Data[i][j] - neg_median)
                        if method == 'UMVUE':
                            SSMD[i][j] = x * (np.nanmean(well_value) / np.nanstd(well_value))
                        elif method == 'MM':
                            SSMD[i][j] = np.nanmean(well_value) / np.nanstd(well_value)
                        else:
                            raise AttributeError('\033[0;31m[ERROR]\033[0m  Method must me UMVUE or MM')

                # # replace NaN with 0
                SSMD = np.nan_to_num(SSMD)

                if verbose:
                    print("Paired SSMD :")
                    print("Systematic Error Corrected Data : ", SECData)
                    print("Data type : ", plate.DataType)
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


def _PairedSSMDr(plate, cNeg, method='UMVUE', SECData=True, verbose=False):
    """
    performed paired SSMDr for plate with replicat
    :param plate: Plate Object to analyze
    :param cNeg: negative control reference
    :param method: which method to use MM or UMVUE
    :param SECData: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return:score data
    """
    try:
        # if no neg was provided raise AttributeError
        if cNeg is None:
            raise AttributeError('\033[0;31m[ERROR]\033[0m  Must provided negative control')
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            SSMDr = np.zeros(plate.PlateSetup.platesetup.shape)

            # # replace 0 with NaN
            SSMDr[SSMDr == 0] = np.NaN

            neg_pos = plate.PlateSetup.getGenePos(cNeg)
            if not neg_pos:
                raise Exception

            # search neg control value
            def _search_neg_data(replicat, Neg_Pos):
                neg_value = []
                for i in range(SSMDr.shape[0]):
                    for j in range(SSMDr.shape[1]):
                        well_value = 0
                        try:
                            if SECData:
                                well_value = replicat.SECData[i][j]
                            else:
                                well_value = replicat.Data[i][j]
                        except Exception:
                            raise Exception("\033[0;31m[ERROR]\033[0m  Your desired datatype are not available")
                        # check if neg value
                        for neg_i in Neg_Pos:
                            if neg_i[0] == i:
                                if neg_i[1] == j:
                                    neg_value.append(well_value)
                return np.nanmedian(neg_value)

            x = (scipy.special.gamma((len(plate.replicat) - 1) / 2) / scipy.special.gamma(
                (len(plate.replicat) - 2) / 2)) * np.sqrt(2 / (len(plate.replicat) - 1))

            try:
                for i in range(SSMDr.shape[0]):
                    for j in range(SSMDr.shape[1]):
                        well_value = []
                        for key, value in plate.replicat.items():
                            neg_median = _search_neg_data(value, neg_pos)
                            if SECData:
                                well_value.append(value.SECDataMedian[i][j] - neg_median)
                            else:
                                well_value.append(value.DataMedian[i][j] - neg_median)
                        if method == 'UMVUE':
                            SSMDr[i][j] = x * (np.nanmedian(well_value) / mad(well_value))
                        elif method == 'MM':
                            SSMDr[i][j] = np.nanmedian(well_value) / mad(well_value)
                        else:
                            raise AttributeError('\033[0;31m[ERROR]\033[0m  Method must me UMVUE or MM')

                # # replace NaN with 0
                SSMDr = np.nan_to_num(SSMDr)

                if verbose:
                    print("Paired SSMDr :")
                    print("Systematic Error Corrected Data : ", SECData)
                    print("Data type : ", plate.DataType)
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


def _SSMD(plate, cNeg, method='UMVUE', SECData=True, verbose=False):
    """
    performed SSMD for plate without replicat
    take dataMean/Median or SECDatadata from plate object
    :param plate: Plate Object to analyze
    :param cNeg: negative control reference
    :param method: which method to use MM or UMVUE
    :param SECData: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return:score data
    """
    try:
        # if no neg was provided raise AttributeError
        if cNeg is None:
            raise AttributeError('Must provided negative control')
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            ps = plate.PlateSetup
            ssmd = np.zeros(ps.platesetup.shape)

            # # replace 0 with NaN
            ssmd[ssmd == 0] = np.NaN

            neg_well = ps.getGenePos(cNeg)
            if not neg_well:
                raise Exception
            neg_data = []
            data = None
            try:
                if SECData:
                    data = plate.SECData
                else:
                    data = plate.Data
            except Exception as e:
                print(e)
            if data is None:
                raise Exception("\033[0;31m[ERROR]\033[0m  Your desired datatype are not available")
            # grab all neg data
            for neg_pos in neg_well:
                neg_data.append(data[neg_pos[0]][neg_pos[1]])
            # check if len is sufficient
            if len(neg_data) < 2:
                raise ValueError('\033[0;31m[ERROR]\033[0m  Insuficient negative data')

            if method == 'MM':
                ssmd = (data - np.nanmean(neg_data)) / (np.sqrt(2) * np.nanstd(neg_data))
            elif method == 'UMVUE':
                k = 2 * (scipy.special.gamma(
                    ((len(neg_data) - 1) / 2) / scipy.special.gamma((len(neg_data) - 2) / 2))) ** 2
                ssmd = (data - np.nanmean(neg_data)) / (np.sqrt((2 / k) * (len(neg_data))) * np.nanstd(neg_data))
            else:
                raise AttributeError('\033[0;31m[ERROR]\033[0m  Method must be MM or UMVUE')

            # # replace NaN with 0
            ssmd = np.nan_to_num(ssmd)

            if verbose:
                print('SSMD without replicat, or inplate data from plate')
                print("Systematic Error Corrected Data : ", SECData)
                print("Data type : ", plate.DataType)
                print("method parameter : ", method)
                print("SSMD score :")
                print(ssmd)
                print("")
            return ssmd
        else:
            raise TypeError
    except Exception as e:
        print(e)


def _SSMDr(plate, cNeg, method='UMVUE', SECData=True, verbose=False):
    """
    perfored  SSMDr for plate without replicat
    take dataMean/Median or SECDatadata from plate object
    :param plate: Plate Object to analyze
    :param cNeg: negative control reference
    :param method: which method to use MM or UMVUE
    :param SECData: use data with Systematic Error Corrected
    :param verbose: be verbose or not
    :return:score data
    """
    try:
        # if no neg was provided raise AttributeError
        if cNeg is None:
            raise AttributeError('\033[0;31m[ERROR]\033[0m  Must provided negative control')
        if isinstance(plate, ScreenPlateReplicatPS.Plate):
            ps = plate.PlateSetup
            ssmdr = np.zeros(ps.platesetup.shape)

            # # replace 0 with NaN
            ssmdr[ssmdr == 0] = np.NaN

            neg_well = ps.getGenePos(cNeg)
            if not neg_well:
                raise Exception
            neg_data = []
            data = None
            try:
                if SECData:
                    data = plate.SECData
                else:
                    data = plate.Data
            except Exception as e:
                print(e)
            if data is None:
                raise Exception("\033[0;31m[ERROR]\033[0m  Your desired datatype are not available")
            # grab all neg data
            for neg_pos in neg_well:
                neg_data.append(data[neg_pos[0]][neg_pos[1]])
            # check if len is sufficient
            if len(neg_data) < 2:
                raise ValueError('Insuficient negative data')

            if method == 'MM':
                ssmdr = (data - np.nanmedian(neg_data)) / (np.sqrt(2) * mad(neg_data))
            elif method == 'UMVUE':
                k = 2 * (scipy.special.gamma(
                    ((len(neg_data) - 1) / 2) / scipy.special.gamma((len(neg_data) - 2) / 2))) ** 2
                ssmdr = (data - np.nanmedian(neg_data)) / (np.sqrt((2 / k) * (len(neg_data))) * mad(neg_data))
            else:
                raise AttributeError('\033[0;31m[ERROR]\033[0m  Method must be MM or UMVUE')


            # # replace NaN with 0
            ssmdr = np.nan_to_num(ssmdr)

            if verbose:
                print('SSMDr without replicat')
                print("Systematic Error Corrected Data : ", SECData)
                print("Data type : ", plate.DataType)
                print("method parameter : ", method)
                print("SSMD score :")
                print(ssmdr)
                print("")
            return ssmdr
        else:
            raise TypeError
    except Exception as e:
        print(e)