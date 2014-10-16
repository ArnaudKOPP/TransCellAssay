__author__ = 'Arnaud KOPP'
"""
In this correction method, the background signal corresponding to each well is calculated by averaging the activities
withing each well across all plate of screen. Then, a polynomial fitting is performed to generate an experiment-wise
background surface for a single screening run. The offset of the background surface from a zero plate is considered to
be the consequence of present systematic errors, and the correction is performed by subtracting the background surface
from each plate data in the screen. The background correction performed on pre-normalized data was found to be more
efficient, and exclusion of the control wells was recommended in the background surface calculations. The detailed
description of the algorithm is found in "Statistical Analysis of Systematic Errors in HTS" Kevorkov and Makarenkov 2005
"""


def BackgroundCorrection():
    try:
        return 0
    except Exception as e:
        print(e)