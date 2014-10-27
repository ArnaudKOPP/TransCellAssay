__author__ = 'Arnaud KOPP'
"""
© 2014 KOPP Arnaud All Rights Reserved

Performed basic Quality control like S/N, Z-factor or SSMD

There are various environmental, instrumental and biological factors that contribute to assay performance in a HT
setting. Therefore, one key the key steps in the analysis of HT screening data is the examination of the assay quality.
To determine if the data collected from each plate meet the minimum quality requirement, and if anny pattern exist
before and after normalization, the distribution of control and test sample data should be examined at
experiment/plate/well level.

We expect good separation between positive and negative control in a plate with good quality.

SSMD,CVD and Z-factor are in robust version
"""
import ScreenPlateReplicatPS
import numpy as np
import pandas as pd
import Statistic.Test.SystematicErrorDetectionTest
from Statistic.Stat import mad


def QualityControl(plate, features, cneg, cpos, SEDT=False, SECdata=False, verbose=False):
    try:
        if not isinstance(plate, ScreenPlateReplicatPS.Plate):
            raise TypeError("\033[0;31m[ERROR]\033[0m")
        else:
            neg_well = plate.PlateSetup.getGeneWell(cneg)
            pos_well = plate.PlateSetup.getGeneWell(cpos)
            for key, value in plate.replicat.items():
                _replicat_quality_control(value, feature=features, cneg=neg_well, cpos=pos_well, SEDT=SEDT,
                                          SECdata=SECdata, verbose=verbose)
    except Exception as e:
        print(e)


def _replicat_quality_control(replicat, feature, cneg, cpos, SEDT=False, SECdata=False, verbose=False):
    try:
        if not isinstance(replicat, ScreenPlateReplicatPS.Replicat):
            raise TypeError("\033[0;31m[ERROR]\033[0m")
        else:
            negdata = _get_data_control(replicat.Data, feature=feature, c_ref=cneg)
            posdata = _get_data_control(replicat.Data, feature=feature, c_ref=cpos)

            if SEDT:
                if SECdata:
                    if replicat.SECDataMean is None:
                        raise ValueError("\033[0;31m[ERROR]\033[0m SEC Before")
                    Statistic.Test.SystematicErrorDetectionTest(replicat.SECDataMean, verbose=True)
                else:
                    if replicat.DataMean is None:
                        replicat.computeDataForFeature(feature)
                    Statistic.Test.SystematicErrorDetectionTest(replicat.DataMean, verbose=True)
            if verbose:
                return 0
    except Exception as e:
        print(e)


def _get_data_control(data, feature, c_ref):
    """
    Grab the data of the desired well
    :param data: data frame
    :param feature: a feature that we want to analyze
    :param c_ref: a control ref list that we want to search, list of well in this format : A1
    :return: 1D array with data from desired Wells
    """
    try:
        if not isinstance(data, pd.DataFrame):
            raise TypeError("\033[0;31m[ERROR]\033[0m Invalide data Format")
        else:
            data = pd.DataFrame()
            for i in c_ref:
                if data.empty:
                    data = data[feature][data['Well'] == i]
                data.append(data[feature][data['Well'] == i])
            return data
    except Exception as e:
        print(e)


def _signal_to_background(cneg, cpos):
    """
    This is a simple measure of the ratio of the positive control mean to the background signal mean (neg control)
    :param cneg: negative control data
    :param cpos: positive control data
    :return: signal to background value
    """
    try:
        sb = np.mean(cpos) / np.mean(cneg)
        return sb
    except Exception as e:
        print(e)


def _signal_to_noise(cneg, cpos):
    """
    This is similar measure to signal_to_background with inclusion of signal variability in the formulation
    :param cneg:
    :param cpos: positive control data
    :return: signal to noise value
    """
    try:
        sn = (np.mean(cpos) - np.mean(cneg)) / np.std(cneg)
        return sn
    except Exception as e:
        print(e)


def _signal_windows(cneg, cpos):
    """
    This is a more indicative measure of the data range in a HTS assay than the abose parameters
    :param cneg: negative control data
    :param cpos: positive control data
    :return: signal windows value
    """
    try:
        sw = (np.abs(np.mean(cpos) - np.mean(cneg)) - 3 * (np.std(cpos) + np.std(cneg))) / np.std(cneg)
        return sw
    except Exception as e:
        print(e)


def _avr(cneg, cpos):
    """
    This parameters capture the data variability in both controls as opposed to signal_windows, and can be defined
    as 1-Z'factor.
    :param cneg: negative control data
    :param cpos: positive control data
    :return: avr value
    """
    try:
        avr = (3 * np.std(cpos) + 3 * np.std(cneg)) / (np.abs(np.mean(cpos) - np.mean(cneg)))
        return avr
    except Exception as e:
        print(e)


def _zfactor_prime(cneg, cpos):
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
    try:
        zfactorprime = 1 - ((3 * mad(cpos) + 3 * mad(cneg)) / (np.abs(np.median(cpos) - np.median(cneg))))
        return zfactorprime
    except Exception as e:
        print(e)


def _zfactor(data, feature, cneg, cpos):
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
    :param data:
    :param feature:
    :param cneg: negative control data
    :param cpos: positive control data
    :return: zfactor value
    """
    try:
        if not isinstance(data, pd.DataFrame):
            raise TypeError("\033[0;31m[ERROR]\033[0m Invalide data Format")
        else:
            zfactor = 1 - ((3 * np.mad(cpos) + 3 * np.mad(data[feature])) / (np.abs(np.median(cpos) - np.median(cneg))))
            return zfactor
    except Exception as e:
        print(e)


def _ssmd(cneg, cpos):
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
    :param cneg: negative control data
    :param cpos: positive control data
    :return: ssmd value
    """
    try:
        ssmd = (np.median(cpos) - np.median(cneg)) / (np.sqrt(mad(cpos) ** 2 - mad(cneg) ** 2))
        return ssmd
    except Exception as e:
        print(e)


def _cvd(cneg, cpos):
    """
    As in original meaning of coefficient of variability for a random variable, CVD represents the relative SD of the
    difference with respect to mean of the difference. The largest the absolut value of CVD between two populations, the
    less the differentiation between the two populations. CVD is the reciprocal of SSMD.
    :param cneg: negative control data
    :param cpos: positive control data
    :return: cvd value
    """
    try:
        cvd = (np.sqrt(mad(cpos) ** 2 - mad(cneg) ** 2)) / (np.median(cpos) - np.median(cneg))
        return cvd
    except Exception as e:
        print(e)