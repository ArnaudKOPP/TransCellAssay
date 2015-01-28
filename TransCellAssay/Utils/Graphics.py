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
            surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=plt.cm.Reds, linewidth=0, antialiased=True)
            fig.colorbar(surf, shrink=0.5, aspect=5)
            ax.invert_yaxis()
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
            ax.bar3d(x_data, y_data, np.zeros(len(z_data)), 1, 1, z_data, color='b', alpha=0.5)
            ax.invert_yaxis()
            plt.show()
    except Exception as e:
        print(e)


def heatmap(array):
    """
    Output a heatmap with seaborn
    :param array: numpy array that represent data
    """
    try:
        import matplotlib
        import pylab
        import numpy as np
        import string

        fig, ax = matplotlib.pyplot.subplots()
        pylab.pcolor(array, cmap=matplotlib.pyplot.cm.Reds, edgecolors='k')
        pylab.colorbar()

        # # tab like display
        ax.invert_yaxis()

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

        b = len(plate.replica)
        if both is True:
            a = 2
        else:
            a = 1
        fig = plt.figure(figsize=(2.*b, 2.*a))

        i = 1
        for key, value in plate.replica.items():
            ax = fig.add_subplot(a, b, i)
            ax.pcolor(value.array, cmap=plt.cm.Reds, edgecolors='k')
            ax.set_title(str(plate.name)+str(value.name))
            # # tab like display
            ax.invert_yaxis()
            if both:
                ax = fig.add_subplot(a, b, i+b)
                ax.pcolor(value.sec_array, cmap=plt.cm.Reds, edgecolors='k')
                ax.set_title(str(plate.name)+str(value.name))
                # # tab like display
                ax.invert_yaxis()
            i += 1
        plt.show()
    except Exception as e:
        print(e)


def heatmap_map(*args, usesec=False):
    """
    plot heatmap of all replica array from given plate
    :param args: plate object or list of plate
    :param usesec: use sec data or not
    """
    try:
        import matplotlib
        import pylab as plt
        import numpy as np

        screen = []
        for arg in args:
            if isinstance(arg, TCA.Plate):
                screen.append(arg)
            elif isinstance(arg, list):
                for elem in arg:
                    if isinstance(elem, TCA.Plate):
                        screen.append(elem)
                    else:
                        raise TypeError('Accept only list of Plate element')
            else:
                raise TypeError('Accept only plate or list of plate')

        n = np.sum([len(x.replica) for x in screen])
        a = np.floor(n**0.5).astype(int)
        b = np.ceil(1.*n/a).astype(int)
        fig = plt.figure(figsize=(2.*b, 2.*a))
        i = 1

        for plate in screen:
            for key, value in plate.replica.items():
                ax = fig.add_subplot(a, b, i)
                if not usesec:
                    ax.pcolor(value.array, cmap=plt.cm.Reds, edgecolors='k')
                    # # tab like display
                    ax.invert_yaxis()
                else:
                    ax.pcolor(value.sec_array, cmap=plt.cm.Reds, edgecolors='k')
                    # # tab like display
                    ax.invert_yaxis()
                ax.set_title(str(plate.name)+' '+str(value.name))
                i += 1
        fig.set_tight_layout(True)

        plt.show()
    except Exception as e:
        print(e)


def heatmap_p(array):
    """
    Output a heatmap with seaborn
    :param array: numpy array that represent data
    """
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        sns.set()
        sns.heatmap(array)
        plt.show()
    except Exception as e:
        print(e)


def plate_heatmap_p(plate, both=True):
    """
    Plate all heatmap for plate object
    :param both: print data and SECdata
    :param plate: plate object with correct data
    """
    try:
        import matplotlib
        import pylab as plt
        import numpy as np
        import seaborn as sns

        b = len(plate.replica)
        if both is True:
            a = 2
        else:
            a = 1
        fig = plt.figure(figsize=(2.*b, 2.*a))

        i = 1
        for key, value in plate.replica.items():
            ax = fig.add_subplot(a, b, i)
            sns.set()
            sns.heatmap(value.array)
            if both:
                ax = fig.add_subplot(a, b, i+b)
                sns.set()
                sns.heatmap(value.sec_array)
            i += 1
        plt.show()
    except Exception as e:
        print(e)


def heatmap_map_p(*args, usesec=False):
    """
    plot heatmap of all replica array from given plate
    :param args: plate object or list of plate
    :param usesec: use sec data or not
    """
    try:
        import matplotlib
        import pylab as plt
        import numpy as np
        import seaborn as sns

        screen = []
        for arg in args:
            if isinstance(arg, TCA.Plate):
                screen.append(arg)
            elif isinstance(arg, list):
                for elem in arg:
                    if isinstance(elem, TCA.Plate):
                        screen.append(elem)
                    else:
                        raise TypeError('Accept only list of Plate element')
            else:
                raise TypeError('Accept only plate or list of plate')

        n = np.sum([len(x.replica) for x in screen])
        a = np.floor(n**0.5).astype(int)
        b = np.ceil(1.*n/a).astype(int)
        fig = plt.figure(figsize=(2.*b, 2.*a))
        i = 1

        for plate in screen:
            for key, value in plate.replica.items():
                ax = fig.add_subplot(a, b, i)
                if not usesec:
                    sns.set()
                    sns.heatmap(value.array)
                else:
                    sns.set()
                    sns.heatmap(value.sec_array)
                ax.set_title(str(plate.name)+' '+str(value.name))
                i += 1
        fig.set_tight_layout(True)

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


def boxplot_by_wells(dataframe, channel):
    """
    plot the boxplot for each well
    :param dataframe:
    :param channel; whiche channel to display
    """
    try:
        import pandas as pd
        import matplotlib.pyplot as plt

        pd.options.display.mpl_style = 'default'
        if isinstance(dataframe, pd.DataFrame):
            bp = dataframe.boxplot(column=channel, by='Well')
            plt.show(block=True)
        else:
            raise TypeError
    except Exception as e:
        print(e)


def plot_multiple_plate(*args, usesec=False, neg=None, pos=None, other=None, marker='o'):
    """
    Plot from all replica from given plate, the array value
    :param args: plate object
    :param usesec: use sec data
    :param neg: neg in green
    :param pos: pos in red
    :param other: some gene in yellow
    :param marker: marker style
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np

        plt_list = []
        for arg in args:
            if isinstance(arg, TCA.Plate):
                plt_list.append(arg)
            elif isinstance(arg, list):
                for elem in arg:
                    if isinstance(elem, TCA.Plate):
                        plt_list.append(elem)
                    else:
                        raise TypeError('Accept only list of Plate element')
            else:
                raise TypeError('Accept only plate or list of plate')

        fig = plt.figure()
        ax = fig.add_subplot(111)
        i = 0
        for plate in plt_list:
            assert isinstance(plate, TCA.Plate)
            for key, value in plate.replica.items():
                # select data
                if usesec:
                    data = value.sec_array.flatten()
                else:
                    data = value.array.flatten()
                # part for neg, pos or other in color
                if neg is not None or pos is not None or other is not None:
                    pm = plate.platemap.platemap.values.flatten()
                    posi = np.random.normal(i, 0.05, len(data))
                    for i in range(len(data)):
                        curr = str(pm[i])
                        if curr == neg:
                            plt.scatter(posi[i], data[i], c='g', marker=marker)
                        elif curr == pos:
                            plt.scatter(posi[i], data[i], c='r', marker=marker)
                        elif curr == other:
                            plt.scatter(posi[i], data[i], c='y', marker=marker)
                        else:
                            plt.scatter(posi[i], data[i], marker=marker)
                # part all in blue
                if neg is None and pos is None and other is None:
                    plt.scatter(np.random.normal(i, 0.05, len(data)), data, marker=marker)
                i += 1
        ax.set_xlim([-0.5, i-0.5])
        ax.set_ylabel('Well value')
        ax.set_xlabel('Plate/Replicat ID')
        plt.show()
    except Exception as e:
        print(e)


def plot_distribution(wells, plate, channel, rep=None, pool=False):
    """
    Plot distribution of multiple well
    :param wells: list of wells to plot distribution
    :param plate: Plate with replica
    :param channel: which channel to plot
    :param rep: if rep is provided, plot only distribution of selected wells for this one
    :param pool: if pool is True, the selected wells are pooled accross replica
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
                    rep_series[rep] = pd.Series(plate[rep].get_raw_data(channel=channel, well=Well))
                    rep_series[rep].name = str(rep)+str(Well)
                else:
                    for key, value in plate.replica.items():
                        rep_series[key] = pd.Series(value.get_raw_data(channel=channel, well=Well))
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
    Plot in 3d raw data with choosen channels
    :param dataframe: dataframe without class label !!
    :param x: x channel
    :param y: y channel
    :param z: z channel
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
    Plot in 3d raw data with choosen channels and with different color by well
    :param single_cell:
    :param dataframe: dataframe without class label !!
    :param x: x channel
    :param y: y channel
    :param z: z channel
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

        assert isinstance(dataframe, TCA.RawData)

        datagp = dataframe.get_groupby_data()
        median = datagp.median()
        median.plot()
        plt.show()
    except Exception as e:
        print(e)