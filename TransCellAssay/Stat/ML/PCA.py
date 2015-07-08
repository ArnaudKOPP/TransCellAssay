# coding=utf-8
"""
Principal Component Analysis (PCA)
"""

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"

import pandas as pd
import numpy as np
import TransCellAssay as TCA


class PCA():
    """

    :param OBJECT:
    :param target:
    """

    def __init__(self, obj_input, target):
        """
        Init PCA
        :param obj_input: can be replicat, plate or screen
        :param target: target of PCA in Well format (A1)
        :return:
        """
        try:
            if isinstance(obj_input, TCA.Replica):
                print("Process PCA on Replica")
                self.rawdata = obj_input.rawdata
            if isinstance(obj_input, TCA.Plate):
                print("Process PCA on Plate")
        except Exception as e:
            print(e)

    def _replicat_pca(self, replica, n_component=3):
        try:
            assert isinstance(replica, TCA.Replica)
            raw_data = replica.rawdata
            data = self._clear_dataframe(raw_data)

            ## DO PCA
            from sklearn.decomposition import PCA

            X = data.as_matrix()
            pca = PCA(n_components=n_component)
            pca.fit(X)
            transf = pca.transform(X)

            pca_score = pca.explained_variance_ratio_
            V = pca.components_

            x_pca_axis, y_pca_axis, z_pca_axis = V.T * pca_score / pca_score.min()
            x_pca_axis, y_pca_axis, z_pca_axis = 3 * V.T

            # eigenvectors and eigenvalues for the from the covariance matrix
            eig_val_cov, eig_vec_cov = np.linalg.eig(pca.get_covariance())

            for i in range(len(eig_val_cov)):
                eigvec_cov = eig_vec_cov[:, i].reshape(1, 3).T

                print('Eigenvector {}: \n{}'.format(i + 1, eigvec_cov))
                print('Eigenvalue {} from covariance matrix: {}'.format(i + 1, eig_val_cov[i]))
                print(40 * '-')

        except Exception as e:
            print(e)

    def _plate_pca(self, plate):
        try:
            assert isinstance(plate, TCA.Plate)
        except Exception as e:
            print(e)

    def _clear_dataframe(self, dataframe, target, to_remove=None):
        """

        :param dataframe:
        :param target:
        :param to_remove:
        :return:
        """
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
        """

        :param dataframe:
        :return:
        """
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


def plot_3d_cloud_point_pca(df, eig_vec, x=None, y=None, z=None):
    """
    Plot in 3d raw data with chosen channels
    :param eig_vec:
    :param df: dataframe without class label !!
    :param x: x channel
    :param y: y channel
    :param z: z channel
    """
    try:
        import pandas as pd
        import numpy as np

        assert isinstance(df, pd.DataFrame)

        from matplotlib import pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from mpl_toolkits.mplot3d import proj3d
        from matplotlib.patches import FancyArrowPatch
        from matplotlib import pyplot as plt

        class Arrow3D(FancyArrowPatch):
            """

            :param xs:
            :param ys:
            :param zs:
            :param args:
            :param kwargs:
            """

            def __init__(self, xs, ys, zs, *args, **kwargs):
                FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
                self._verts3d = xs, ys, zs

            def draw(self, renderer):
                xs3d, ys3d, zs3d = self._verts3d
                xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
                self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
                FancyArrowPatch.draw(self, renderer)

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        plt.rcParams['legend.fontsize'] = 10
        ax.plot(df[x], df[y], df[z], '.', markersize=4, color='blue', alpha=0.5, label='Raw Data')
        mean_x = np.mean(df[x])
        mean_y = np.mean(df[y])
        mean_z = np.mean(df[z])
        ax.plot([mean_x], [mean_y], [mean_z], 'o', markersize=10, color='red', alpha=0.5)
        for v in eig_vec.T:
            a = Arrow3D([mean_x, v[0]], [mean_y, v[1]], [mean_z, v[2]], mutation_scale=20, lw=3, arrowstyle="-|>",
                        color="r")
            ax.add_artist(a)

        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_zlabel(z)

        plt.title('Raw Data point')
        ax.legend(loc='upper right')
        plt.show()
    except Exception as e:
        print(e)