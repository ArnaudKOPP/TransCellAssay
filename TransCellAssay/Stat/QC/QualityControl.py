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
mean of the group comes from the 99.73% confidence limit. While Z'factor account for the variability in the
control wells, positional effects or any other variability in the sample wells are not captured. Although Z'factor
is an intuitive method to determine the assay quality, several concerns were raised about the reliability of this
parameter as an assay quality measure. Major issue associated with the Z'factor method are that the magnitude of
the Z'factor does not necessarily correlate with the hit confirmation rates, and that Z'factor is not appropriate
measure to compare the assay quality across different screens and assay types.

Z-Factor
This is the modified version of the Z’-factor, where the mean and std of the
negative control are substituted with the ones for the test samples. Although Z-factor
is more advantageous than Z’-factor due to its ability to incorporate sample variability
in the calculations, other issues associated with Z’-factor (as discussed above) still
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

import numpy as np
import pandas as pd
import TransCellAssay as TCA
import logging

log = logging.getLogger(__name__)

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2017 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"


def plates_quality_control(plates, channel, cneg, cpos, sec_data=False):
    """
    Compute quality control on multiple plates for channel
    :param plates: Plate to compute quality object
    :param channel: channel on which we performed quality control
    :param cneg: negative control Name
    :param cpos: positive control Name
    :param sec_data: use sec data
    :return: return dataframe with qc
    """
    assert isinstance(plates, list)

    DF = []
    for plate in plates:
        DF.append(plate_quality_control(plate, channel=channel, cneg=cneg, cpos=cpos, sec_data=sec_data))

    return pd.concat(DF)


def plate_quality_control(plate, channel, cneg, cpos, sec_data=False):
    """
    Compute quality control on plate for selected channel
    :param plate: Plate to compute quality object
    :param channel: channel on which we performed quality control
    :param cneg: negative control Name
    :param cpos: positive control Name
    :param sec_data: use sec data
    :return: return dataframe with qc
    """
    assert isinstance(plate, TCA.Core.Plate)

    plate.agg_data_from_replica_channel(channel=channel, forced_update=True, use_sec_data=sec_data)

    if plate._is_cutted:
        log.error('Plate was cutted, plate analysis cannot be performed : ABORT')
        return 0
    try:
        neg_well = plate.platemap.search_coord(cneg)
        pos_well = plate.platemap.search_coord(cpos)
    except KeyError:
        log.error('Some Reference are non existing : ABORT')
        return 0

    X = pd.DataFrame()

    log.info('Perform quality control on {}'.format(plate.name))

    for repname, replica in plate.replica.items():

        valid_neg_well = [TCA.get_opposite_well_format(x) for x in neg_well]
        valid_pos_well = [TCA.get_opposite_well_format(x) for x in pos_well]

        log.debug('Perform quality control on {}'.format(replica.name))

        # # get Data
        if sec_data and replica.isNormalized:
            negdata = __get_data_control_array(replica.array_c, c_ref=valid_neg_well)
            posdata = __get_data_control_array(replica.array_c, c_ref=valid_pos_well)
        else:
            negdata = __get_data_control_array(replica.array, c_ref=valid_neg_well)
            posdata = __get_data_control_array(replica.array, c_ref=valid_pos_well)

        qc_rep_data = pd.DataFrame(
            np.zeros(1, dtype=[('Replicat ID', str), ('Neg Mean', float), ('Neg SD', float), ('Pos Mean', float),
                               ('Pos SD', float), ('Plate Mean', float), ('Plate SD', float)]))

        qc_rep_data['Replicat ID'] = "{0}--{1}".format(plate.name, replica.name)
        qc_rep_data['Neg Mean'] = np.mean(negdata)
        qc_rep_data['Neg SD'] = np.std(negdata)
        qc_rep_data['Pos Mean'] = np.mean(posdata)
        qc_rep_data['Pos SD'] = np.std(posdata)
        if sec_data and replica.isNormalized:
            qc_rep_data['Plate Mean'] = np.mean(replica.array_c.flatten())
            qc_rep_data['Plate SD'] = np.std(replica.array_c.flatten())
        else:
            qc_rep_data['Plate Mean'] = np.mean(replica.array.flatten())
            qc_rep_data['Plate SD'] = np.std(replica.array.flatten())
        X = X.append(qc_rep_data)

    X.loc[:, "AVR"] = (3 * X["Pos SD"] + 3 * X["Neg SD"]) / np.abs(X["Pos Mean"] - X["Neg Mean"])
    X.loc[:, "ZFactor*"] = 1 - (3 * X["Pos SD"] + 3 * X["Neg SD"]) / np.abs(X["Pos Mean"] - X["Neg Mean"])
    X.loc[:, "ZFactor"] = 1 - (3 * X["Pos SD"] + 3 * X["Plate SD"]) / np.abs(X["Pos Mean"] - X["Neg Mean"])
    X.loc[:, "SSMD"] = (X["Pos Mean"] - X["Neg Mean"]) / np.sqrt(np.abs(X["Pos SD"] ** 2 - X["Neg SD"] ** 2))
    X.loc[:, "CVD"] = np.sqrt(np.abs(X["Pos SD"] ** 2 - X["Neg SD"] ** 2)) / (X["Pos Mean"] - X["Neg Mean"])

    return X


def __get_data_control_array(array, c_ref):
    """
    Grab value from array with from specified position
    :param array: array
    :param c_ref: ref in well format (A1)
    :return: 1d array with data from desired Wells
    """
    data = list()
    for i in c_ref:
        if isinstance(i, str):
            i = TCA.get_opposite_well_format(i)
        data.append(array[i[0]][i[1]])
    return data
