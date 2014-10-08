__author__ = 'Arnaud KOPP'
"""
Define method for median polish, this algo is used for removing edge effect
"""
import numpy as np
from scipy import stats

class MedianPolish:
    """
    Fits an additive model using Tukey's median polish algorithm
    Chapter 10 of Tukey, John W (1977). Exploratory Data Analysis. Addison-Wesley. ISBN 0-201-07616-0.
    """

    def __init__(self, array):
        """Get numeric data from numpy ndarray to self.tbl, keep the original copy in tbl_org"""
        if isinstance(array, np.ndarray):
            self.tbl_org = array
            self.tbl = self.tbl_org.copy()
        else:
            raise TypeError('Expected the argument to be a numpy.ndarray.')

    def median_polish(self, max_iterations=10, method='median'):
        """
            Implements Tukey's median polish alghoritm for additive models
            method - default is median, alternative is mean. That would give us result equal ANOVA.
            With non full plate, it work for the moment only with entire empty col or Row
        """
        # # replace 0 with NaN
        self.tbl[self.tbl == 0] = np.NaN
        grand_effect = 0
        median_row_effects = 0
        median_col_effects = 0
        row_effects = np.zeros(shape=self.tbl.shape[0])
        col_effects = np.zeros(shape=self.tbl.shape[1])

        for i in range(max_iterations):
            if method == 'median':
                row_medians = stats.nanmedian(self.tbl, 1)
                row_effects += row_medians
                median_row_effects = stats.nanmedian(row_effects)
            elif method == 'average':
                row_medians = stats.nanmean(self.tbl, 1)
                row_effects += row_medians
                median_row_effects = stats.nanmean(row_effects)
            grand_effect += median_row_effects
            row_effects -= median_row_effects
            self.tbl -= row_medians[:, np.newaxis]

            if method == 'median':
                col_medians = stats.nanmedian(self.tbl, 0)
                col_effects += col_medians
                median_col_effects = stats.nanmedian(col_effects)
            elif method == 'average':
                col_medians = stats.nanmean(self.tbl, 0)
                col_effects += col_medians
                median_col_effects = stats.nanmean(col_effects)

            self.tbl -= col_medians

            grand_effect += median_col_effects
        # # replace NaN with 0
        self.tbl = np.nan_to_num(self.tbl)
        return grand_effect, col_effects, row_effects, self.tbl, self.tbl_org


