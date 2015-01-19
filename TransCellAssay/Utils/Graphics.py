# coding=utf-8
"""
Method for making graphics of plate
"""
import TransCellAssay as TCA

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "CC BY-NC-ND 4.0 License"
__version__ = "1.0"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"
__status__ = "Production"


def plot_plate_3d(array, surf=False):
    """
    Make a 3d histogramme plot of matrix representing plate, give an array(in matrix form) of value (whatever you want)
    :param surf: surface or histogram
    :param array: numpy array
    :return:show 3d plot
    """
    try:
        if surf:
            from mpl_toolkits.mplot3d import Axes3D
            from matplotlib import cm
            import matplotlib.pyplot as plt
            import numpy as np

            fig = plt.figure()
            x = np.arange(array.shape[1])
            y = np.arange(array.shape[0])
            x, y = np.meshgrid(x, y)
            z = array
            ax = fig.gca(projection='3d')
            surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='hot', linewidth=0, antialiased=False)
            fig.colorbar(surf, shrink=0.5, aspect=5)
            plt.show()
        else:
            from mpl_toolkits.mplot3d import Axes3D
            import matplotlib.pyplot as plt
            import numpy as np

            data_array = np.array(array)
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            x_data, y_data = np.meshgrid(np.arange(data_array.shape[1]), np.arange(data_array.shape[0]))
            #
            # Flatten out the arrays so that they may be passed to "ax.bar3d".
            # Basically, ax.bar3d expects three one-dimensional arrays:
            # x_data, y_data, z_data. The following call boils down to picking
            # one entry from each array and plotting a bar to from
            # (x_data[i], y_data[i], 0) to (x_data[i], y_data[i], z_data[i]).
            #
            x_data = x_data.flatten()
            y_data = y_data.flatten()
            z_data = data_array.flatten()
            ax.bar3d(x_data, y_data, np.zeros(len(z_data)), 1, 1, z_data)
            plt.show()
    except Exception as e:
        print(e)


def heatmap(array, pretty=True):
    """
    Output a heatmap with seaborn
    :param pretty: use Seaborn or matplotlib
    :param array: numpy array that represent data
    """
    try:
        if pretty:
            import matplotlib.pyplot as plt
            import seaborn as sns
            sns.set()
            sns.heatmap(array)
            plt.show()
        else:
            import matplotlib
            import pylab
            import numpy as np

            # Create new colormap, with white for zero
            # (can also take RGB values, like (255,255,255):
            colors = [('white')] + [(pylab.cm.jet(i)) for i in range(1, 256)]
            new_map = matplotlib.colors.LinearSegmentedColormap.from_list('new_map', colors, N=256)

            pylab.pcolor(array, cmap=new_map)
            pylab.colorbar()
            pylab.show()
    except Exception as e:
        print(e)


def plate_heatmap(plate, both=True):
    """
    Plate all heatmap for plate object
    :param both: print data and SECdata
    :param plate: plate object with correct data
    """
    try:
        import matplotlib
        import pylab as plt
        import numpy as np

        b = len(plate.replicat)
        if both is True:
            a = 2
        else:
            a = 1
        fig = plt.figure(figsize=(2.*b, 2.*a))

        # Create new colormap, with white for zero
        # (can also take RGB values, like (255,255,255):
        colors = [('white')] + [(plt.cm.jet(i)) for i in range(1, 256)]
        new_map = matplotlib.colors.LinearSegmentedColormap.from_list('new_map', colors, N=256)

        i = 1
        for key, value in plate.replicat.items():
            ax = fig.add_subplot(a, b, i)
            ax.pcolor(value.Data, cmap=new_map)
            ax.set_title(str(plate.Name)+str(value.name))
            if both:
                ax = fig.add_subplot(a, b, i+b)
                ax.pcolor(value.SECData, cmap=new_map)
                ax.set_title(str(plate.Name)+str(value.name))
            i += 1
        plt.show()
    except Exception as e:
        print(e)


def systematic_error(array):
    """
    plot systematic error in cols and rows axis
    :param array: take a numpy array in input
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np

        rowmean = []
        rowstd = []
        colmean = []
        colstd = []
        if isinstance(array, np.ndarray):
            for row in range(array.shape[0]):
                rowmean.append(np.mean(array[row, :]))
                rowstd.append(np.std(array[row, :]))
            for col in range(array.shape[1]):
                colmean.append(np.mean(array[:, col]))
                colstd.append(np.std(array[:, col]))

            fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(10, 5))

            row = np.arange(array.shape[0])
            col = np.arange(array.shape[1])
            ax0.bar(row, rowmean, color='r', yerr=rowstd)
            ax1.bar(col, colmean, color='r', yerr=colstd)

            ax0.set_ylabel('Mean')
            ax0.set_title('Mean by row')
            ax1.set_ylabel('Mean')
            ax1.set_title('Mean by Col')

            plt.show()
        else:
            raise TypeError
    except Exception as e:
        print(e)


def boxplot_by_wells(dataframe, feature):
    """
    plot the boxplot for each well
    :param dataframe:
    :param feature; whiche feature to display
    """
    try:
        import pandas as pd
        import matplotlib.pyplot as plt

        pd.options.display.mpl_style = 'default'
        if isinstance(dataframe, pd.DataFrame):
            bp = dataframe.boxplot(column=feature, by='Well')
            plt.show(block=True)
        else:
            raise TypeError
    except Exception as e:
        print(e)


def plot_screen(screen):
    """

    :param screen:
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np

        if isinstance(screen, TCA.Core.Screen):
            fig = plt.figure()
            ax = fig.add_subplot(111)
            mxm = 0
            for i in range(screen.shape[0]):
                for j in range(screen.shape[1]):
                    I = 0
                    platedata = list()
                    platenumber = list()
                    for key, value in screen.plate.items():
                        for repkey, repvalue in value.replicat.items():
                            platedata.append(np.log2(repvalue.DataMedian[i][j]))
                            platenumber.append(I)
                            I += 1
                    ax.plot(platenumber, platedata, 'b.')
                    mxm = I
            ax.set_xlim([-1, mxm])
            ax.set_ylabel('Log Data')
            ax.set_xlabel('Plate/Replicat ID')
            plt.show()
        else:
            raise TypeError("\033[0;31m[ERROR]\033[0m Must Provided a Screen")
    except Exception as e:
        print(e)


def plot_distribution(wells, plate, feature, rep=None, pool=False):
    """
    Plot distribution of multiple well
    :param wells: list of wells to plot distribution
    :param plate: Plate with replicat
    :param feature: which feature to plot
    :param rep: if rep is provided, plot only distribution of selected wells for this one
    :param pool: if pool is True, the selected wells are pooled accross replicat
    """
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
        import TransCellAssay.Core

        pd.options.display.mpl_style = 'default'
        if isinstance(plate, TCA.Core.Plate):
            for Well in wells:
                rep_series = dict()
                if rep is not None:
                    rep_series[rep] = pd.Series(plate[rep].RawData[feature][plate[rep].RawData['Well'] == Well])
                    rep_series[rep].name = str(rep)+str(Well)
                else:
                    for key, value in plate.replicat.items():
                        rep_series[key] = pd.Series(value.RawData[feature][value.RawData['Well'] == Well])
                        rep_series[key].name = key+str(Well)
                # # Plotting with pandas
                if pool:
                    pooled_data = pd.Series()
                    for key, value in rep_series.items():
                        pooled_data = pooled_data.append(value)
                    pooled_data.name = str(Well)
                    pooled_data.plot(kind='hist', alpha=0.5, legend=True, bins=1000)
                else:
                    for key, value in rep_series.items():
                        value.plot(kind='hist', alpha=0.5, legend=True, bins=1000)
            plt.show(block=True)
    except Exception as e:
        print(e)


def plot_3d_cloud_point(dataframe, x=None, y=None, z=None):
    """
    Plot in 3d raw data with choosen features
    :param dataframe: dataframe without class label !!
    :param x: x feature
    :param y: y feature
    :param z: z feature
    """
    try:
        import pandas as pd

        assert isinstance(dataframe, pd.DataFrame)

        from matplotlib import pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from mpl_toolkits.mplot3d import proj3d

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        plt.rcParams['legend.fontsize'] = 10
        ax.plot(dataframe[x], dataframe[y], dataframe[z], '.', markersize=4, color='blue', alpha=0.5, label='Raw Data')

        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_zlabel(z)

        plt.title('Raw Data point')
        ax.legend(loc='upper right')
        plt.show()
    except Exception as e:
        print(e)


def plot_3d_per_well(dataframe, x=None, y=None, z=None, single_cell=True):
    """
    Plot in 3d raw data with choosen features and with different color by well
    :param single_cell:
    :param dataframe: dataframe without class label !!
    :param x: x feature
    :param y: y feature
    :param z: z feature
    """
    try:
        import pandas as pd
        import numpy as np

        assert isinstance(dataframe, pd.DataFrame)

        from matplotlib import pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from mpl_toolkits.mplot3d import proj3d

        wells = dataframe.Well.unique()
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        plt.rcParams['legend.fontsize'] = 10
        for well in wells:
            if not single_cell:
                ax.plot(dataframe[x][dataframe['Well'] == well],
                        dataframe[y][dataframe['Well'] == well],
                        dataframe[z][dataframe['Well'] == well], '.', markersize=4, color='blue', alpha=0.5,
                        label='Raw Data')
            else:
                ax.plot(np.median(dataframe[x][dataframe['Well'] == well]),
                        np.median(dataframe[y][dataframe['Well'] == well]),
                        np.median(dataframe[z][dataframe['Well'] == well]), '.', markersize=4, color='blue', alpha=0.5,
                        label='Raw Data')
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_zlabel(z)

        plt.title('Raw Data point')
        ax.legend(loc='upper right')
        plt.show()
    except Exception as e:
        print(e)


'''
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(data["Nuc Area"][data["Well"] == 'A1'], data["Nuc Intensity"][data["Well"] == 'A1'], data["Cell Intensity"][data["Well"] == 'A1'], '.', color='blue', alpha=0.5, label='E1')
ax.scatter(data["Nuc Area"][data["Well"] == 'B1'], data["Nuc Intensity"][data["Well"] == 'B1'], data["Cell Intensity"][data["Well"] == 'B1'], '.', color='red', alpha=0.1, label='B1')

plt.title('Raw Data point')
ax.legend(loc='upper right')
plt.show()
'''


def plot_raw_data(dataframe):
    """
    DataFrame must be clean of unwanted columns
    :param dataframe:
    """
    try:
        import pandas as pd
        from matplotlib import pyplot as plt

        assert isinstance(dataframe, pd.DataFrame)

        datagp = dataframe.groupby("Well")
        median = datagp.median()
        median.plot()
        plt.show()
    except Exception as e:
        print(e)