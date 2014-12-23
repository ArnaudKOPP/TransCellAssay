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
import TransCellAssay as TCA


class LDA():
    def __init__(self, OBJECT, target):
        """
        Init LDA
        :param OBJECT: can be replicat, plate or screen
        :param target: target of LDA in Well format (A1)
        :return:
        """
        try:
            if isinstance(OBJECT, TCA.Replicat):
                print("Process LDA on Replicat")
                self.rawdata = OBJECT.RawData
            if isinstance(OBJECT, TCA.Plate):
                print("Process LDA on Plate")
            if isinstance(OBJECT, TCA.Screen):
                print("Process LDA on Screen")
        except Exception as e:
            print(e)

    def _replicat_LDA(self, replicat, n_component=3):
        try:
            assert isinstance(replicat, TCA.Replicat)
            raw_data = replicat.RawData
            data = self._clear_dataframe(raw_data)

            ## DO LDA
            from sklearn.lda import LDA

            X = data.as_matrix()
            LDA = LDA(n_components=n_component)
            LDA.fit(X)
            transf = LDA.transform(X)

        except Exception as e:
            print(e)

    def _plate_LDA(self, plate):
        try:
            assert isinstance(plate, TCA.Plate)
        except Exception as e:
            print(e)

    def _screen_LDA(self, screen):
        try:
            assert isinstance(screen, TCA.Screen)
        except Exception as e:
            print(e)

    def _clear_dataframe(self, dataframe, target, to_remove=None):
        try:
            # remove class label (Well columns)
            dataframe = dataframe.drop("Well", 1)
            if to_remove is not None:
                for col in to_remove:
                    dataframe = dataframe.drop(col, 1)
            return dataframe[dataframe['Well'] == target]
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
        """
        Plot the raw data in 3d
        :param x:
        :param y:
        :param z:
        :return:
        """
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