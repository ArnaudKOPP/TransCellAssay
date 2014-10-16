__author__ = 'Arnaud KOPP'
"""
This method follows an analogous strategy of the background correction method; however, a least-squares approximation
or polynomial fitting is performed independently for each well across all plates. The fitted value are then subtracted
from each data point to obtain the corrected data set. In a study comparing the systematic error correction method, well
correction was found to be the most effective for successful hit selection.
"""


def WellCorrection():
    try:
        return 0
    except Exception as e:
        print(e)