"""
Linear Discriminant Analysis (LDA)
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"

import pandas as pd
import numpy as np
import scipy
import TransCellAssay as TCA


class LCA():
    def __init__(self, Data):
        try:
            if isinstance(Data, TCA.Replicat):
                print("Process LCA on Replicat")
            if isinstance(Data, TCA.Plate):
                print("Process LCA on Plate")
            if isinstance(Data, TCA.Screen):
                print("Process LCA on Screen")
        except Exception as e:
            print(e)

    def _replicat_lca(self, replicat):
        try:
            assert isinstance(replicat, TCA.Replicat)
            data = replicat.Dataframe
        except Exception as e:
            print(e)

    def _plate_pca(self, plate):
        try:
            assert isinstance(plate, TCA.Plate)
        except Exception as e:
            print(e)

    def _screen_pca(self, screen):
        try:
            assert isinstance(screen, TCA.Screen)
        except Exception as e:
            print(e)