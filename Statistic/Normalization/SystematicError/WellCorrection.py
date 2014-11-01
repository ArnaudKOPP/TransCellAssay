"""
This method follows an analogous strategy to the background correction method; however, a least-squares approximation
or polynomial fitting is performed independently for each well accross all plates. The fitted value are then substracted
from each data point to obtain the corrected data set. In a study comparing the systematic error correction methods
discussed so far, well-correction method was found to be the most effective for succesful "hit" selection.

The well correction method consist of two main steps:
    -Least-squares approximation of the data carried out separatly for each well of the array(screen)
    -Zscore normalization of the data within each well location of the assay

For the analysis of large industrial assays, more sophisticated function like higher degree polynomial or spline
functions can also be used.
Experimental values for a specific well location can be also have ascending or descending trends. The well correction
procedure first discovers these trends using the linear least-squares approximation; note that fitting by a polynomial
approximation of a higher degree can be also carried out instead of the linear approximation. Thus, the obtained trend
(a straight line y = ax + b in case of the linear fitting, where x denotes the plate number and y denotes the plate
normalized measurement ) is subtracted from or added to the original measurement bringing te mean value of this well
to zero
"""

import Core
import numpy as np

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


class WellCorrection():
    def __init__(self, screen):
        if isinstance(screen, Core.Screen):
            self.screen = screen
        else:
            raise TypeError

    def wellcorrection(self, approx="lst", apply_on='replicat', verbose=False):
        try:
            self._apply_approx()
            self._apply_zscore()
        except Exception as e:
            print(e)

    def _apply_approx(self, approx="lst", apply_on='replicat', verbose=False):
        try:
            if apply_on == "Plate":
                # iterate on all plate
                for key, value in self.screen.PlateList.items():
                    # check if plate object
                    if not isinstance(value, Core.Plate):
                        raise TypeError("\033[0;31m[ERROR]\033[0m Must provided good object")
                    else:
                        return 0

            elif apply_on == "Replicat":
                objectCnt = 0
                # iterate on all plate
                for key, value in self.screen.PlateList.items():
                    # check if plate object
                    if not isinstance(value, Core.Plate):
                        raise TypeError("\033[0;31m[ERROR]\033[0m Must provided good object")
                    else:
                        # iterate on all replicat in the plate
                        for repName, repValue in value.replicat.items():
                            if not isinstance(repValue, Core.Replicat):
                                raise TypeError
                            else:
                                return 0
            else:
                raise AttributeError("\033[0;31m[ERROR]\033[0m Apply strategy only on plate or replicat")
        except Exception as e:
            print(e)

    def _apply_zscore(self, data):

        try:
            datax = (data - np.mean(data)) / np.std(data)
            return datax
        except Exception as e:
            print(e)

    def _compute_approximation(self, data_y, approx="lst", verbose=False):
        try:
            if approx == "lst":
                n = len(data_y)
                data_x = np.arange(n)
                B = np.array(data_y)
                A = np.array(([[data_x[j], 1] for j in range(n)]))
                X = np.linalg.lstsq(A, B)[0]
                if verbose:
                    a = X[0]
                    b = X[1]
                    print("Line is: y=", a, "x+", b)
                return X
            if approx == "pol":
                from numpy import polynomial as P

                n = len(data_y)
                data_x = np.arange(n)
                c, stats = P.polyfit(data_x, data_y, 5, full=True)
                if verbose:
                    print(c, stats)
                return c, stats
            if approx == "spline":
                from scipy.interpolate import UnivariateSpline

                n = len(data_y)
                data_x = np.arange(n)
                s = UnivariateSpline(data_x, data_y, s=1)
                xs = np.arange(n)
                if verbose:
                    print(xs)
                ys = s(xs)
                return ys
        except Exception as e:
            print(e)