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
    def __init__(self, OBJECT, target):
        """
        Init PCA
        :param OBJECT: can be replicat, plate or screen
        :param target: target of PCA in Well format (A1)
        :return:
        """
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

    def _replicat_pca(self, replicat, n_component=3):
        try:
            assert isinstance(replicat, TCA.Replicat)
            raw_data = replicat.Dataframe
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

    def _screen_pca(self, screen):
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


def plot_3d_cloud_point_pca(DataFrame, eig_vec, x=None, y=None, z=None):
    """
    Plot in 3d raw data with choosen features
    :param DataFrame: dataframe without class label !!
    :param x: x feature
    :param y: y feature
    :param z: z feature
    """
    try:
        import pandas as pd
        import numpy as np

        assert isinstance(DataFrame, pd.DataFrame)

        from matplotlib import pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from mpl_toolkits.mplot3d import proj3d
        from matplotlib.patches import FancyArrowPatch
        from matplotlib import pyplot as plt

        class Arrow3D(FancyArrowPatch):
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
        ax.plot(DataFrame[x], DataFrame[y], DataFrame[z], '.', markersize=4, color='blue', alpha=0.5, label='Raw Data')
        mean_x = np.mean(DataFrame[x])
        mean_y = np.mean(DataFrame[y])
        mean_z = np.mean(DataFrame[z])
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