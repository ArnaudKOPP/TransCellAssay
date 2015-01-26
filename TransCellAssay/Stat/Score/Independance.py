# coding=utf-8
"""
Calculates the T-test for the means of TWO INDEPENDENT samples of scores.
This is a two-sided test for the null hypothesis that 2 independent samples have identical average (expected) values.
This test assumes that the populations have identical variances.

We can use this test, if we observe two independent samples from the same or different population, e.g. exam scores of
boys and girls or of two ethnic groups. The test measures whether the average (expected) value differs significantly
across samples. If we observe a large p-value, for example larger than 0.05 or 0.1, then we cannot reject the null
hypothesis of identical average scores. If the p-value is smaller than the threshold, e.g. 1%, 5% or 10%, then we
reject the null hypothesis of equal averages.
"""
from scipy import stats
import TransCellAssay as TCA
import numpy as np

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Dev"


def independance(plate, neg, channel, equal_var=True):
    """
    Perform t-test againt neg reference for all well of plate/replica, work only for plate with one replicat
    :param plate: Plate object
    :param neg: negtive reference
    :param channel: on which channel to test
    :param equal_var: equal variance or not
    :return: numpy array with result
    """
    try:
        if not isinstance(plate, TCA.Plate):
            raise TypeError('Need a Plate Object')
        else:
            if len(plate.replica) > 1:
                raise NotImplementedError('Implemented only for one replicat for the moment')

        shape = plate.platemap.platemap.get_shape()
        size = shape[0] * shape[1]
        result_array = np.zeros(size, dtype=[('GeneName', object), ('T-Statistic', float),
                                             ('Two-tailed P-Value', float)])

        for key, value in plate.replica.items():
            neg_well = value.get_valid_well(neg)
            neg_data = value.get_raw_data(channel=channel, well=neg_well)
            cpt = 0
            for i in range(shape[0]):
                for j in range(shape[1]):
                    test = value.get_raw_data(channel=channel, well=TCA.get_opposite_well_format((i, j)))
                    res = stats.ttest_ind(neg_data, test, equal_var=equal_var)
                    result_array['GeneName'][cpt] = plate.platemap.values[i][j]
                    result_array['T-Statistic'][cpt] = res[0]
                    result_array['Two-Tailed P-Value'][cpt] = res[1]
                cpt += 1

        return result_array
    except Exception as e:
        print("\033[0;31m[ERROR]\033[0m", e)