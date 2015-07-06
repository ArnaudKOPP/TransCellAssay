# coding=utf-8
"""
Method for making graphics of plate
"""
import TransCellAssay as TCA
import warnings

__author__ = "Arnaud KOPP"
__copyright__ = "© 2014-2015 KOPP Arnaud All Rights Reserved"
__credits__ = ["KOPP Arnaud"]
__license__ = "GPLv3"
__maintainer__ = "Arnaud KOPP"
__email__ = "kopp.arnaud@gmail.com"

warnings.simplefilter('always', DeprecationWarning)

def array_surf_3d(*args, array):
    """
    Make a 3d surface plot of matrix representing plate, give an array(in matrix form) of value (whatever you want)
    :param array: numpy array
    :return:show 3d plot
    """
    try:
        import numpy as np
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import cm
        import matplotlib.pyplot as plt

        fig = plt.figure()
        x = np.arange(array.shape[1])
        y = np.arange(array.shape[0])
        x, y = np.meshgrid(x, y)
        z = array
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=plt.cm.Reds,
                               linewidth=0, antialiased=True,alpha=0.5)
        fig.colorbar(surf, shrink=0.5, aspect=5)
        ax.invert_yaxis()
        plt.show(block=True)
    except Exception as e:
        print(e)

def arrays_surf_3d(*args):
    """
    Make a 3d surface plot of matrix representing plate, give a list of array (with same size) and limited to 4
    :param args: list of array, limit to 4
    :return:show 3d plot
    """
    try:
        import numpy as np
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import cm
        import matplotlib.pyplot as plt

        fig = plt.figure()
        ax = fig.gca(projection='3d')

        cmap = (plt.cm.Reds, plt.cm.Blues, plt.cm.BuGn, plt.cm.BuPu)
        i = 0

        for arg in args:
            assert isinstance(arg, np.ndarray)
            x = np.arange(arg.shape[1])
            y = np.arange(arg.shape[0])
            x, y = np.meshgrid(x, y)
            z = arg
            surf = ax.plot_surface(x, y, z, rstride=1, cstride=1,cmap=cmap[i],
                                   linewidth=0, antialiased=True,alpha=0.2)
            fig.colorbar(surf, shrink=0.5, aspect=5)
            i += 1
        ax.invert_yaxis()
        plt.show(block=True)
    except Exception as e:
        print(e)

def array_hist_3d(array):
    """
    Make a 3d histogramme plot of matrix representing plate, give an array(in matrix form) of value (whatever you want)
    :param array: numpy array
    :return:show 3d plot
    """
    try:
        import numpy as np
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt

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
        plt.show(block=True)
    except Exception as e:
        print(e)

def heatmap(array, file_path=None):
    """
    Output a heatmap with matplotlib
    :param array: numpy array that represent data
    """
    warnings.warn("Shouldn't use this function anymore! use _p function", DeprecationWarning)
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

        if file_path is not None:
            pylab.savefig(file_path)
        else:
            pylab.show(block=True)
    except Exception as e:
        print(e)

def plate_heatmap(plate, both=False, file_path=None):
    """
    Plate all heatmap for plate object
    :param both: print data and SECdata
    :param plate: plate object with correct data
    """
    warnings.warn("Shouldn't use this function anymore! use _p function", PendingDeprecationWarning)
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
        if file_path is not None:
            plt.savefig(file_path)
        else:
            plt.show(block=True)
    except Exception as e:
        print(e)

def plates_heatmap(*args, usesec=False, file_path=None):
    """
    plot heatmap of all replica array from given plate
    :param args: plate object or list of plate
    :param usesec: use sec data or not
    """
    warnings.warn("Shouldn't use this function anymore! use _p function", PendingDeprecationWarning)
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

        if file_path is not None:
            plt.savefig(file_path)
        else:
            plt.show(block=True)
    except Exception as e:
        print(e)

def heatmap_p(array, file_path=None):
    """
    Output a heatmap with seaborn
    :param array: numpy array that represent data
    """
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        sns.set()
        sns.heatmap(array)
        if file_path is not None:
            plt.savefig(file_path)
        else:
            plt.show(block=True)
    except Exception as e:
        print(e)

def plate_heatmap_p(plate, both=False, file_path=None):
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
        if file_path is not None:
            plt.savefig(file_path)
        else:
            plt.show(block=True)
    except Exception as e:
        print(e)

def plates_heatmap_p(*args, usesec=False, file_path=None):
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

        if file_path is not None:
            plt.savefig(file_path)
        else:
            plt.show(block=True)
    except Exception as e:
        print(e)

def systematic_error(array, file_path=None):
    """
    plot systematic error in cols and rows axis
    :param array: take a numpy array in input
    """
    import numpy as np
    assert isinstance(array, np.ndarray)
    try:
        import matplotlib.pyplot as plt

        rowmean = []
        rowstd = []
        colmean = []
        colstd = []
        for row in range(array.shape[0]):
            rowmean.append(np.mean(array[row, :]))
            rowstd.append(np.std(array[row, :]))
        for col in range(array.shape[1]):
            colmean.append(np.mean(array[:, col]))
            colstd.append(np.std(array[:, col]))

        fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(10, 5))

        row = np.arange(array.shape[0])
        col = np.arange(array.shape[1])
        ax0.bar(row, rowmean, color='c', yerr=rowstd)
        ax1.bar(col, colmean, color='c', yerr=colstd)

        ax0.spines["top"].set_visible(False)
        ax0.spines["bottom"].set_visible(False)
        ax0.spines["right"].set_visible(False)
        ax0.spines["left"].set_visible(False)
        ax1.spines["top"].set_visible(False)
        ax1.spines["bottom"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.spines["left"].set_visible(False)

        ax0.set_ylabel('Mean')
        ax0.set_title('Mean by row')
        ax1.set_ylabel('Mean')
        ax1.set_title('Mean by Col')

        plt.tick_params(axis="both", which="both", bottom="off", top="off",
                labelbottom="on", left="off", right="off", labelleft="on")

        if file_path is not None:
            plt.savefig(file_path)
        else:
            plt.show(block=True)
    except Exception as e:
        print(e)

def boxplot_by_wells(rawdata, channel, file_path=None):
    """
    plot the boxplot for each well
    :param rawdata:
    :param channel; whiche channel to display
    """
    assert isinstance(rawdata, TCA.Core.RawData)
    try:
        import pandas as pd
        import matplotlib.pyplot as plt

        pd.options.display.mpl_style = 'default'
        bp = rawdata.df.boxplot(column=channel, by='Well')
        if file_path is not None:
            plt.savefig(file_path)
        else:
            plt.show(block=True)
    except Exception as e:
        print(e)

def well_count(replica, file_path=None):
    """

    :param rawdata:
    :param file_path:
    :return:
    """
    assert isinstance(replica, TCA.Core.Replica)
    try:
        import pandas as pd
        import matplotlib.pyplot as plt

        pd.options.display.mpl_style = 'default'

        dfgb = replica.rawdata.get_groupby_data()
        dfgb.size().plot(kind='bar')

        if file_path is not None:
            plt.savefig(file_path)
        else:
            plt.show(block=True)

    except Exception as e:
        print(e)

def well_sorted(replica, well, channel, file_path=None):
    """

    :param plate:
    :param file_path:
    :return:
    """
    assert isinstance(replica, TCA.Core.Replica)
    try:
        import pandas as pd
        import matplotlib.pyplot as plt

        pd.options.display.mpl_style = 'default'

        df = replica.get_rawdata(channel=channel, well=well)
        df_sorted = df.sort(inplace=False)
        df_sorted = df_sorted.reset_index()
        df_sorted = df_sorted.drop('index', 1)
        df_sorted.plot()

        if file_path is not None:
            plt.savefig(file_path, dpi=200)
        else:
            plt.show(block=True)

    except Exception as e:
        print(e)

def plate_well_count(plate, file_path=None):
    """

    :param plate:
    :param file_path:
    :return:
    """
    assert isinstance(plate, TCA.Core.Plate)
    try:
        import pandas as pd
        import matplotlib.pyplot as plt

        pd.options.display.mpl_style = 'default'

        b = len(plate.replica)
        a = 1
        fig = plt.figure(figsize=(2.*b, 2.*a))

        i = 1
        for key, value in plate.replica.items():
            assert isinstance(value, TCA.Core.Replica)
            ax = fig.add_subplot(a, b, i)
            df = value.rawdata.df
            df.groupby('Well').size().plot(kind='bar')
            ax.set_title(str(plate.name)+' '+str(value.name))
            i += 1
        if file_path is not None:
            plt.savefig(file_path)
        else:
            plt.show(block=True)

    except Exception as e:
        print(e)

def dual_flashlight_plot(y, x):
    """
    x and y array
    :param y: array
    :param x: array
    """
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.scatter(y.flatten(), x.flatten())
    plt.show(block=True)
    pass

def plot_wells(*args, usesec=False, neg=None, pos=None, other=None, marker='o', width=0.1, file_path=None):
    """
    Plot from all replica from given plate, the array value
    :param args: plate object
    :param usesec: use sec data
    :param neg: neg in green
    :param pos: pos in red
    :param other: some gene in yellow
    :param marker: marker style
    :param width: width of plate value
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
                    posi = np.random.normal(i, width, len(data))
                    for j in range(len(data)):
                        curr = str(pm[j])
                        if curr == neg:
                            plt.scatter(posi[j], data[j], c='g', marker=marker)
                        elif curr == pos:
                            plt.scatter(posi[j], data[j], c='r', marker=marker)
                        elif curr == other:
                            plt.scatter(posi[j], data[j], c='y', marker=marker)
                        else:
                            plt.scatter(posi[j], data[j], marker='.')
                # part all in blue
                if neg is None and pos is None and other is None:
                    plt.scatter(np.random.normal(i, width, len(data)), data, marker=marker)
                i += 1
        ax.set_xlim([-0.5, i-0.5])
        ax.set_ylabel('Well value')
        ax.set_xlabel('Plate/Replica ID')
        if file_path is not None:
            plt.savefig(file_path)
        else:
            plt.show(block=True)
    except Exception as e:
        print(e)

def plot_distribution_hist(wells, plate, channel, rep=None, pool=False, bins=100, file_path=None):
    """
    Plot distribution of multiple well with hist
    :param wells: list of wells to plot distribution
    :param plate: Plate with replica
    :param channel: which channel to plot
    :param rep: if rep is provided, plot only distribution of selected wells for this one
    :param pool: if pool is True, the selected wells are pooled accross replica
    """
    assert isinstance(plate, TCA.Core.Plate)
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
        import TransCellAssay.Core

        pd.options.display.mpl_style = 'default'
        for Well in wells:
            rep_series = dict()
            if rep is not None:
                rep_series[rep] = pd.Series(plate[rep].get_rawdata(channel=channel, well=Well))
                rep_series[rep].name = str(rep)+str(Well)
            else:
                for key, value in plate.replica.items():
                    rep_series[key] = pd.Series(value.get_rawdata(channel=channel, well=Well))
                    rep_series[key].name = key+str(Well)
            # # Plotting with pandas
            if pool:
                pooled_data = pd.Series()
                for key, value in rep_series.items():
                    pooled_data = pooled_data.append(value)
                pooled_data.name = str(Well)
                pooled_data.plot(kind='hist', alpha=0.5, legend=True, bins=bins)
            else:
                for key, value in rep_series.items():
                    value.plot(kind='hist', alpha=0.5, legend=True, bins=bins)
        if file_path is not None:
            plt.savefig(file_path)
        else:
            plt.show(block=True)
    except Exception as e:
        print(e)

def plot_distribution_kde(plate, wells, channel, rep=None, pool=False, file_path=None):
    """
    Plot distribution of multiple well with kde
    :param plate: Plate with replica
    :param wells: list of wells to plot distribution
    :param channel: which channel to plot
    :param rep: if rep is provided, plot only distribution of selected wells for this one
    :param pool: if pool is True, the selected wells are pooled accross replica
    :param file_path: saving location
    """
    assert isinstance(plate, TCA.Core.Plate)
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
        import TransCellAssay.Core

        pd.options.display.mpl_style = 'default'
        for Well in wells:
            rep_series = dict()
            if rep is not None:
                rep_series[rep] = pd.Series(plate[rep].get_rawdata(channel=channel, well=Well))
                rep_series[rep].name = str(rep)+str(Well)
            else:
                for key, value in plate.replica.items():
                    rep_series[key] = pd.Series(value.get_rawdata(channel=channel, well=Well))
                    rep_series[key].name = key+str(Well)
            # # Plotting with pandas
            if pool:
                pooled_data = pd.Series()
                for key, value in rep_series.items():
                    pooled_data = pooled_data.append(value)
                pooled_data.name = str(Well)
                pooled_data.plot(kind='kde', alpha=0.5, legend=True)
            else:
                for key, value in rep_series.items():
                    value.plot(kind='kde', alpha=0.5, legend=True)
        if file_path is not None:
            plt.savefig(file_path)
        else:
            plt.show(block=True)
    except Exception as e:
        print(e)

def plot_3d_cloud_point(title, x, y, z, x_label='x', y_label='y', z_label='z'):
    """
    Plot in 3d three array of data
    :param x: x array
    :param y: y array
    :param z: z array
    """
    try:
        import numpy as np
        from matplotlib import pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from mpl_toolkits.mplot3d import proj3d

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        plt.rcParams['legend.fontsize'] = 10
        ax.plot(x, y, z, '.', markersize=4, color='blue', alpha=0.5, label='Point')

        ax.set_xlabel(str(x_label))
        ax.set_ylabel(str(y_label))
        ax.set_zlabel(str(z_label))

        plt.title(str(title))
        ax.legend(loc='upper right')
        plt.show(block=True)
    except Exception as e:
        print(e)

def plot_3d_per_well(rawdata, x, y, z, single_cell=True, skip_wells=[]):
    """
    Plot in 3d raw data with choosen channels and with different color by well
    :param single_cell: plot all cell or only median
    :param rawdata: raw data object
    :param x: x channel
    :param y: y channel
    :param z: z channel
    :param skip_wells: skip some wells if wanted
    """
    assert isinstance(rawdata, TCA.Core.RawData)
    try:
        import pandas as pd
        import numpy as np
        from matplotlib import pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from mpl_toolkits.mplot3d import proj3d

        wells = rawdata.get_unique_well()
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        plt.rcParams['legend.fontsize'] = 10
        for well in wells:
            if well not in skip_wells :
                if single_cell:
                    ax.plot(rawdata.df[x][rawdata.df['Well'] == well].values,
                            rawdata.df[y][rawdata.df['Well'] == well].values,
                            rawdata.df[z][rawdata.df['Well'] == well].values, '.', markersize=4, alpha=0.5,
                            label=str(well))
                else:
                    ax.plot([np.median(rawdata.df[x][rawdata.df['Well'] == well].values)],
                            [np.median(rawdata.df[y][rawdata.df['Well'] == well].values)],
                            [np.median(rawdata.df[z][rawdata.df['Well'] == well].values)], '.', markersize=4, alpha=0.5,
                            label=str(well))
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_zlabel(z)

        plt.title('Raw Data point')
        ax.legend(loc='upper right')
        plt.show(block=True)
    except Exception as e:
        print(e)
