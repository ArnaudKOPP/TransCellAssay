"""
Principal Component Analysis (PCA)
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
import TransCellAssay as TCA


class PCA():
    def __init__(self, OBJECT):
        try:
            if isinstance(OBJECT, TCA.Replicat):
                print("Process PCA on Replicat")
                self.rawdata = OBJECT.Dataframe
            if isinstance(OBJECT, TCA.Plate):
                print("Process PCA on Plate")
            if isinstance(OBJECT, TCA.Screen):
                print("Process PCA on Screen")
        except Exception as e:
            print(e)

    def _replicat_pca(self, replicat, n_component=5):
        try:
            assert isinstance(replicat, TCA.Replicat)
            raw_data = replicat.Dataframe
            data = self._clear_dataframe(raw_data)

            from sklearn.decomposition import PCA

            X = data.as_matrix()
            pca = PCA(n_components=n_component)
            pca.fit(X)

            transf = pca.transform(X)


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

    def _clear_dataframe(self, dataframe, to_remove=None):
        try:
            # remove class label (Well columns)
            dataframe = dataframe.drop("Well", 1)
            if to_remove is not None:
                for col in to_remove:
                    dataframe = dataframe.drop(col, 1)
            return dataframe
        except Exception as e:
            print(e)

    def _mean_vector(self, dataframe):
        try:
            assert isinstance(dataframe, pd.DataFrame)
            median = dataframe.median(axis=0)
            mean_vector = median.values
            return mean_vector
        except Exception as e:
            print(e)

    def _plot_rawdata(self, x, y, z):
        try:
            assert isinstance(self.rawdata, pd.DataFrame)
            if x or y or z is None:
                raise ValueError("Must provided x y z columns argument")

            from matplotlib import pyplot as plt
            from mpl_toolkits.mplot3d import Axes3D
            from mpl_toolkits.mplot3d import proj3d

            fig = plt.figure(figsize=(8, 8))
            ax = fig.add_subplot(111, projection='3d')
            plt.rcParams['legend.fontsize'] = 10
            ax.plot(self.rawdata[x], self.rawdata[y], self.rawdata[z], '.', markersize=4, color='blue',
                    alpha=0.5, label='Raw Data')

            plt.title('Raw Data point')
            ax.legend(loc='upper right')
            plt.show()
        except Exception as e:
            print(e)