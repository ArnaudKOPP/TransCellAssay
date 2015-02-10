# coding=utf-8
"""
Performed basic Quality control like S/N, Z-factor, SSMD and CVD

There are various environmental, instrumental and biological factors that contribute to assay performance in a HT
setting. Therefore, one key the key steps in the analysis of HT screening data is the examination of the assay quality.
To determine if the data collected from each plate meet the minimum quality requirement, and if anny pattern exist
before and after normalization, the distribution of control and test sample data should be examined at
experiment/plate/well level.
We expect good separation between positive and negative control in a plate with good quality.

AVR
This parameters capture the data variability in both controls as opposed to signal_windows, and can be defined
as 1-Z'factor.

Z'Factor
Despite of the fact that AVR and Z'factor has similar properties, the latter is the most widely used QC criterion,
where the separation between positive and negative controls is calculated as a measure of the signal range of a
particular assay in a single plate. Z'factor has its basis on normality assumption, and the use of 3 std's of the
mean of the group comes from the 99.73% confidence limit. While Z'factor account for the variablity in the
control wells, positional effects or any other variability in the sample wells are not captured. Although Z'factor
is an intuitive method to determine the assay quality, several concerns were raised about the reliability of this
parameter as an assay quality measure. Major issue associated with the Z'factor method are that the magnitude of
the Z'factor does not necessarily correlate with the hit confirmation rates, and that Z'factor is not appropriate
measure to compare the assay quality across different screens and assay types.

Z-Factor
This is the modified version of the Z’-factor, where the mean and std of the
negative control are substituted with the ones for the test samples. Although Z-factor
is more advantageous than Z’-factor due to its ability to incorporate sample variabili‐
ty in the calculations, other issues associated with Z’-factor (as discussed above) still
apply. Additionally, in a focused library in which many possible “hits” are clustered
in certain plates, Z-factor would not be an appropriate QC parameter. While assays
with Z’- or Z-factor values above 0.5 are considered to be excellent, one may want to
include additional measures, such as visual inspection or more advanced formulations
in the decision process, especially for cell-based assays with inherently high signal
variability.

SSMD
It is an alternative quality metric to Z’- and Z-factor, which was recently devel‐
oped to assess the assay quality in HT screens (Zhang 2007a; Zhang 2007b). Due to its ba‐
sis on probabilistic and statistical theories, SSMD was shown to be a more meaningful
parameter than previously mentioned methods for QC purposes. SSMD differs from Z’-
and Z-factor by its ability to handle controls with different effects, which enables the se‐
lection of multiple QC criteria for assays (Zhang et al. 2008a). The application of SSMD-
based QC criterion was demonstrated in multiple studies in comparison to other
commonly-used methods (Zhang 2008b; Zhang 2011b; Zhang et al. 2008a). Although
SSMD was developed primarily for RNAi screens, it can also be used for small molecule
screens.
The larger the absolute value of SSMD between two populations, the greater the differentiation  between the two
populations

CVD
As in original meaning of coefficient of variability for a random variable, CVD represents the relative SD of the
difference with respect to mean of the difference.
The largest the absolute value of CVD between two populations, the less the differentiation between the two
populations. CVD is the reciprocal of SSMD.

SSMD,CVD and Z-factor are in robust version
"""

import os
import numpy as np
import pandas as pd
import TransCellAssay as TCA


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def plate_quality_control(plate, channel, cneg, cpos, sedt=False, sec_data=False, use_raw_data=True, dirpath=None,
                          skipping_wells=True, verbose=False):
    """
    Compute quality control on plate for selected channel
    :param plate: Plate to compute quality object
    :param channel: channel on which we performed quality control
    :param cneg: negative control Name
    :param cpos: positive control Name
    :param sedt: systematic error detection test
    :param sec_data: use sec data or not for sedt
    :param use_raw_data: use 1data/Well data
    :param dirpath: directory path for saving data
    :param skipping_wells: skipped defined wells
    :param verbose: print or not quality data
    :return: return numpy array with qc
    """
    if not isinstance(plate, TCA.Core.Plate):
        raise TypeError("Need A Plate")
    else:
        if plate._is_cutted:
            print('\033[0;31m[ERROR]\033[0m Plate was cutted, plate analysis cannot be performed : ABORT')
            return 0
        try:
            neg_well = plate.platemap.search_coord(cneg)
            pos_well = plate.platemap.search_coord(cpos)
        except KeyError:
            print('\033[0;31m[ERROR]\033[0m Some Reference are non existing : ABORT')
            return 0

        qc_data_array = pd.DataFrame()

        for key, value in plate.replica.items():
            qc_data_array = qc_data_array.append(
                __replicat_quality_control(value, channel=channel, neg_well=neg_well, pos_well=pos_well,
                                           sedt=sedt, sec_data=sec_data, use_raw_data=use_raw_data,
                                           skipping_wells=skipping_wells,  verbose=False))

        if verbose:
            print("Quality control for plate: ", plate.name + "\n")
            print(qc_data_array)

        if dirpath is not None:
            qc_data_array.to_csv(os.path.join(dirpath, "QC_Data.csv"), index=False)

        return qc_data_array


def __replicat_quality_control(replicat, channel, neg_well, pos_well, sedt=False, sec_data=False, use_raw_data=True,
                               skipping_wells=True, verbose=False):
    """
    Compute quality control on replicat for selected channel
    :param replicat: Replicat to compute qc
    :param channel: channel on which we performed quality control
    :param neg_well: negative control well
    :param pos_well: positive control well
    :param sedt: systematic error detection test
    :param sec_data: use sec data or not for sedt
    :param use_raw_data: use 1data/Well data
    :param skipping_wells: skipped defined wells
    :param verbose: print or not quality data
    :return:return numpy array with qc
    """
    if not use_raw_data:
        if replicat.array is None:
            raise Exception("Compute_data_from_replicat First")

    if skipping_wells:
        valid_neg_well = replicat.get_valid_well(neg_well)
        valid_pos_well = replicat.get_valid_well(pos_well)
    else:
        valid_neg_well = [TCA.get_opposite_well_format(x) for x in neg_well]
        valid_pos_well = [TCA.get_opposite_well_format(x) for x in pos_well]

    # # get Data
    if not use_raw_data:
        if replicat.array is not None:
            negdata = __get_data_control_array(replicat.array, c_ref=valid_neg_well)
            posdata = __get_data_control_array(replicat.array, c_ref=valid_pos_well)
        else:
            print('\033[0;33m[WARNING]\033[0m 1data/well not available, using instead Raw Data')
            negdata = __get_data_control(replicat.rawdata, channel=channel, c_ref=valid_neg_well)
            posdata = __get_data_control(replicat.rawdata, channel=channel, c_ref=valid_pos_well)
    else:
        if replicat.rawdata is not None:
            negdata = __get_data_control(replicat.rawdata, channel=channel, c_ref=valid_neg_well)
            posdata = __get_data_control(replicat.rawdata, channel=channel, c_ref=valid_pos_well)
        else:
            print('\033[0;33m[WARNING]\033[0m Raw Data not available, using instead 1data/well ')
            negdata = __get_data_control_array(replicat.array, c_ref=valid_neg_well)
            posdata = __get_data_control_array(replicat.array, c_ref=valid_pos_well)

    qc_data_array = pd.DataFrame(
        np.zeros(1, dtype=[('Replicat ID', str), ('Neg Mean', float), ('Neg SD', float),
                           ('Pos Mean', float), ('Pos SD', float), ('AVR', float),
                           ('Z*Factor', float), ('ZFactor', float), ('SSMD', float),
                           ('CVD', float)]))

    if sedt:
        if sec_data:
            if replicat.sec_array is None:
                raise ValueError("SEC Before")
            else:
                TCA.systematic_error_detection_test(replicat.sec_array)
        else:
            TCA.systematic_error_detection_test(replicat.array, verbose=True)
    qc_data_array['Replicat ID'] = replicat.name
    qc_data_array['Neg Mean'] = np.mean(negdata)
    qc_data_array['Neg SD'] = np.std(negdata)
    qc_data_array['Pos Mean'] = np.mean(posdata)
    qc_data_array['Pos SD'] = np.std(posdata)
    qc_data_array['AVR'] = __avr(negdata, posdata)
    qc_data_array['Z*Factor'] = __zfactor_prime(negdata, posdata)
    qc_data_array['ZFactor'] = __zfactor(replicat.rawdata.df, channel, negdata, posdata)
    qc_data_array['SSMD'] = __ssmd(negdata, posdata)
    qc_data_array['CVD'] = __cvd(negdata, posdata)

    if verbose:
        print("\nQuality Control for replicat : ", replicat.name + "\n")
        print(qc_data_array)
    return qc_data_array


def __get_data_control_array(array, c_ref):
    """
    Grab value from array with from specified position
    :param array: array
    :param c_ref: ref in well format (A1)
    :return: 1d array with data from desired Wells
    """
    if not isinstance(array, np.ndarray):
        raise TypeError("Invalide data Format")
    else:
        data = list()
        for i in c_ref:
            if isinstance(i, str):
                i = TCA.get_opposite_well_format(i)
            data.append(array[i[0]][i[1]])
        return data


def __get_data_control(data, channel, c_ref):
    """
    Grab the data of the desired well
    :param data: data frame
    :param channel: a channel that we want to analyze
    :param c_ref: a control ref list that we want to search, list of well in this format : A1
    :return: 1D array with data from desired Wells
    """
    if not isinstance(data, TCA.RawData):
        raise TypeError("Invalide data Format")
    else:
        datax = pd.DataFrame()
        for i in c_ref:
            if isinstance(i, tuple):
                i = TCA.get_opposite_well_format(i)
            if datax.empty:
                datax = data.get_raw_data(channel=channel, well=i, well_idx=False)
            datax = data.get_raw_data(channel=channel, well=i, well_idx=False)
        return datax


def __avr(cneg, cpos):
    """
    Assay Variability ratio
    This parameters capture the data variability in both controls as opposed to signal_windows, and can be defined
    as 1-Z'factor.
    :param cneg: negative control data
    :param cpos: positive control data
    :return: avr value
    """
    avr = (3 * np.std(cpos) + 3 * np.std(cneg)) / (np.abs(np.mean(cpos) - np.mean(cneg)))
    return avr


def __zfactor_prime(cneg, cpos):
    """
    Despite of the fact that AVR and Z'factor has similar properties, the latter is the most widely used QC criterion,
    where the separation between positive and negative controls is calculated as a measure of the signal range of a
    particular assay in a single plate. Z'factor has its basis on normality assumption, and the use of 3 std's of the
    mean of the group comes from the 99.73% confidence limit. While Z'factor account for the variablity in the
    control wells, positional effects or any other variability in the sample wells are not captured. Although Z'factor
    is an intuitive method to determine the assay quality, several concerns were raised about the reliability of this
    parameter as an assay quality measure. Major issue associated with the Z'factor method are that the magnitude of
    the Z'factor does not necessarily correlate with the hit confirmation rates, and that Z'factor is not appropriate
    measure to compare the assay quality across different screens and assay types.
    :param cneg: negative control data
    :param cpos: positive control data
    :return: z'factor value
    """
    zfactorprime = 1 - ((3 * np.std(cpos) + 3 * np.std(cneg)) / (np.abs(np.mean(cpos) - np.mean(cneg))))
    return zfactorprime


def __zfactor(data, channel, cneg, cpos):
    """
    This is the modified version of the Z’-factor, where the mean and std of the
    negative control are substituted with the ones for the test samples. Although Z-factor
    is more advantageous than Z’-factor due to its ability to incorporate sample variabili‐
    ty in the calculations, other issues associated with Z’-factor (as discussed above) still
    apply. Additionally, in a focused library in which many possible “hits” are clustered
    in certain plates, Z-factor would not be an appropriate QC parameter. While assays
    with Z’- or Z-factor values above 0.5 are considered to be excellent, one may want to
    include additional measures, such as visual inspection or more advanced formulations
    in the decision process, especially for cell-based assays with inherently high signal
    variability.
    :param data: all data from replicat
    :param channel: channel to take data
    :param cneg: negative control data
    :param cpos: positive control data
    :return: zfactor value
    """
    zfactor = 1 - ((3 * np.std(cpos) + 3 * np.std(data[channel])) / (np.abs(np.mean(cpos) - np.mean(cneg))))
    return zfactor


def __ssmd(cneg, cpos):
    """
    It is an alternative quality metric to Z’- and Z-factor, which was recently devel‐
    oped to assess the assay quality in HT screens (Zhang 2007a; Zhang 2007b). Due to its ba‐
    sis on probabilistic and statistical theories, SSMD was shown to be a more meaningful
    parameter than previously mentioned methods for QC purposes. SSMD differs from Z’-
    and Z-factor by its ability to handle controls with different effects, which enables the se‐
    lection of multiple QC criteria for assays (Zhang et al. 2008a). The application of SSMD-
    based QC criterion was demonstrated in multiple studies in comparison to other
    commonly-used methods (Zhang 2008b; Zhang 2011b; Zhang et al. 2008a). Although
    SSMD was developed primarily for RNAi screens, it can also be used for small molecule
    screens.
    The larger the absolute value of SSMD between two populations, the greater the differentiation  between the two
    populations
    :param cneg: negative control data
    :param cpos: positive control data
    :return: ssmd value
    """
    ssmd = (np.mean(cpos) - np.mean(cneg)) / (np.sqrt(np.abs(np.std(cpos) ** 2 - np.std(cneg) ** 2)))
    return ssmd


def __cvd(cneg, cpos):
    """
    As in original meaning of coefficient of variability for a random variable, CVD represents the relative SD of the
    difference with respect to mean of the difference.
    The largest the absolute value of CVD between two populations, the less the differentiation between the two
    populations. CVD is the reciprocal of SSMD.
    :param cneg: negative control data
    :param cpos: positive control data
    :return: cvd value
    """
    cvd = (np.sqrt(np.abs(np.std(cpos) ** 2 - np.std(cneg) ** 2))) / (np.mean(cpos) - np.mean(cneg))
    return cvd
