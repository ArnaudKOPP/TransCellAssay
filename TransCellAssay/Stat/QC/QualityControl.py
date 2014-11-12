"""
Performed basic Quality control like S/N, Z-factor or SSMD

There are various environmental, instrumental and biological factors that contribute to assay performance in a HT
setting. Therefore, one key the key steps in the analysis of HT screening data is the examination of the assay quality.
To determine if the data collected from each plate meet the minimum quality requirement, and if anny pattern exist
before and after normalization, the distribution of control and test sample data should be examined at
experiment/plate/well level.

We expect good separation between positive and negative control in a plate with good quality.

SSMD,CVD and Z-factor are in robust version
"""

import numpy as np
import pandas as pd
import TransCellAssay as TCA


__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def PlateQualityControl(plate, features, cneg, cpos, SEDT=False, SECdata=False, verbose=False):
    try:
        if not isinstance(plate, TCA.Core.Plate):
            raise TypeError("\033[0;31m[ERROR]\033[0m")
        else:
            neg_well = plate.PlateMap.getGeneWell(cneg)
            pos_well = plate.PlateMap.getGeneWell(cpos)

            qc_data_array = pd.DataFrame()

            for key, value in plate.replicat.items():
                qc_data_array = qc_data_array.append(
                    ReplicatQualityControl(value, feature=features, cneg=neg_well, cpos=pos_well,
                                           SEDT=SEDT, SECdata=SECdata, verbose=False))

            if verbose:
                print("\nQuality control for plat: \n")
                print(qc_data_array)
    except Exception as e:
        print(e)


def ReplicatQualityControl(replicat, feature, cneg, cpos, SEDT=False, SECdata=False, verbose=False):
    try:
        if not isinstance(replicat, TCA.Core.Replicat):
            raise TypeError("\033[0;31m[ERROR]\033[0m")
        else:
            negdata = _get_data_control(replicat.Dataframe, feature=feature, c_ref=cneg)
            posdata = _get_data_control(replicat.Dataframe, feature=feature, c_ref=cpos)

            qc_data_array = pd.DataFrame(np.zeros(1,
                                                  dtype=[('Replicat ID', str), ('AVR', float), ('Z*Factor', float),
                                                         ('ZFactor', float), ('SSMD', float), ('CVD', float)]))

            if SEDT:
                if SECdata:
                    if replicat.SECData is None:
                        raise ValueError("\033[0;31m[ERROR]\033[0m SEC Before")
                    TCA.Stat.Test.SystematicErrorDetectionTest(replicat.SECData, verbose=True)

            print("Replicat : ", replicat.name)
            print("mean neg :", np.mean(negdata), " Standard dev : ", np.std(negdata))
            print("mean pos :", np.mean(posdata), " Standard dev : ", np.std(posdata))
            qc_data_array['Replicat ID'] = replicat.name
            qc_data_array['AVR'] = _avr(negdata, posdata)
            qc_data_array['Z*Factor'] = _zfactor_prime(negdata, posdata)
            qc_data_array['ZFactor'] = _zfactor(replicat.Dataframe, feature, negdata, posdata)
            qc_data_array['SSMD'] = _ssmd(negdata, posdata)
            qc_data_array['CVD'] = _cvd(negdata, posdata)

            if verbose:
                print("\nQuality Control for replicat : ", replicat.name)
                print(qc_data_array)
            return qc_data_array
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
            datax = pd.DataFrame()
            for i in c_ref:
                if datax.empty:
                    datax = data[feature][data['Well'] == i]
                datax.append(data[feature][data['Well'] == i])
            return datax
    except Exception as e:
        print(e)


def _avr(cneg, cpos):
    """
    Assay Variability ratio
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
        zfactorprime = 1 - ((3 * np.std(cpos) + 3 * np.std(cneg)) / (np.abs(np.mean(cpos) - np.mean(cneg))))
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
    :param data: all data from replicat
    :param feature: feature to take data
    :param cneg: negative control data
    :param cpos: positive control data
    :return: zfactor value
    """
    try:
        if not isinstance(data, pd.DataFrame):
            raise TypeError("\033[0;31m[ERROR]\033[0m Invalide data Format")
        else:
            zfactor = 1 - ((3 * np.std(cpos) + 3 * np.std(data[feature])) / (np.abs(np.mean(cpos) - np.mean(cneg))))
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

    The larger the absolute value of SSMD between two populations, the greater the differentiation  between the two
    populations
    :param cneg: negative control data
    :param cpos: positive control data
    :return: ssmd value
    """
    try:
        ssmd = (np.mean(cpos) - np.mean(cneg)) / (np.sqrt(np.abs(np.std(cpos) ** 2 - np.std(cneg) ** 2)))
        return ssmd
    except Exception as e:
        print(e)


def _cvd(cneg, cpos):
    """
    As in original meaning of coefficient of variability for a random variable, CVD represents the relative SD of the
    difference with respect to mean of the difference.

    The largest the absolute value of CVD between two populations, the less the differentiation between the two
    populations. CVD is the reciprocal of SSMD.
    :param cneg: negative control data
    :param cpos: positive control data
    :return: cvd value
    """
    try:
        cvd = (np.sqrt(np.abs(np.std(cpos) ** 2 - np.std(cneg) ** 2))) / (np.mean(cpos) - np.mean(cneg))
        return cvd
    except Exception as e:
        print(e)