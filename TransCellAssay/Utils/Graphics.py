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

def Arrays3D(*args, sec_data=False):
    """
    Make a 3d surface plot of matrix representing plate, give a list of array (with same size) and limited to 4
    :param args: list of object (plate or replica), limit to 4
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
            from TransCellAssay.Core.GenericPlate import GenericPlate
            assert isinstance(arg, GenericPlate)

            if sec_data & bool(arg.array_c is not None):
                array = arg.array_c
            else:
                array = arg.array

            x = np.arange(array.shape[1])
            y = np.arange(array.shape[0])
            x_data, y_data = np.meshgrid(x, y)
            z = array
            surf = ax.plot_surface(x_data, y_data, z, rstride=1, cstride=1,cmap=cmap[i],
                                   linewidth=0, antialiased=True,alpha=0.2)
            fig.colorbar(surf, shrink=0.5, aspect=5)
            i += 1

        ax.invert_yaxis()
        plt.show(block=True)
    except Exception as e:
        print(e)

def Array3D(obj, kind="hist", sec_data=False):
    """
    Make a 3d representation of plaque or replica object
    param kind: can be a 3d histogram of 3d surface
    param sec_data: use or not SEC data if available
    """
    from TransCellAssay.Core.GenericPlate import GenericPlate
    assert isinstance(obj, GenericPlate)

    kind_list = ["hist", "surf"]
    assert kind in kind_list, "{0} type not available, use instead {1}".format(kind, kind_list)

    if sec_data & bool(obj.array_c is not None):
        array = obj.array_c
    else:
        array = obj.array

    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    import matplotlib.pyplot as plt

    fig = plt.figure()
    x = np.arange(array.shape[1])
    y = np.arange(array.shape[0])

    if kind == "surf":
        x_data, y_data = np.meshgrid(x, y)
        z = array
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(x_data, y_data, z, rstride=1, cstride=1, cmap=plt.cm.Reds,
                               linewidth=0, antialiased=True,alpha=0.5)
        fig.colorbar(surf, shrink=0.5, aspect=5)
    else:
        ax = fig.add_subplot(111, projection='3d')
        data_array = np.array(array)
        x_data, y_data = np.meshgrid(x, y)
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

    plt.show(block=True)

def HeatMap(obj, render="matplotlib", fpath=None, annot=True, size=(17,12), fmt='d', sec_data=False):
    """
    Create a heatmap from plate or replica object
    """
    from TransCellAssay.Core.GenericPlate import GenericPlate
    assert isinstance(obj, GenericPlate)

    render_list = ["matplotlib", "seaborn"]
    assert render in render_list, "{0} render not available, use instead {1}".format(render, render_list)

    if sec_data & bool(obj.array_c is not None):
        to_print = obj.array_c
    else:
        to_print = obj.array

    if render == "matplotlib":
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=size)
        plt.pcolor(to_print, cmap=plt.cm.Reds, edgecolors='k')
        plt.colorbar()

        # # tab like display
        ax.invert_yaxis()

    else:
        import matplotlib.pyplot as plt
        import seaborn as sns

        fig, ax = plt.subplots(figsize=size)
        sns.set()
        sns.heatmap(to_print, cmap="YlGnBu", annot=annot, fmt=fmt)

    if fpath is not None:
        plt.savefig(fpath, dpi=500)
        plt.close()
    else:
        plt.show(block=True)

def HeatMapPlate(plate, sec_data=False, fpath=None, size=3., render="matplotlib"):
    """
    Make heatmap of array from all replica of given plate object
    """
    import matplotlib
    import pylab as plt
    import numpy as np

    assert isinstance(plate, TCA.Plate)

    render_list = ["matplotlib", "seaborn"]
    assert render in render_list, "{0} render not available, use instead {1}".format(render, render_list)

    b = len(plate.replica)
    if sec_data:
        a = 2
    else:
        a = 1
    fig = plt.figure(figsize=(size*b*1.5, size*a))
    i = 1
    for key, value in plate:
        if render == "matplotlib":
            ax = fig.add_subplot(a, b, i)
            ax.pcolor(value.array, cmap=plt.cm.Reds, edgecolors='k')
            ax.set_title(str(plate.name)+" "+str(value.name))
            # # tab like display
            ax.invert_yaxis()
            if sec_data:
                ax = fig.add_subplot(a, b, i+b)
                ax.pcolor(value.array_c, cmap=plt.cm.Reds, edgecolors='k')
                ax.set_title(str(plate.name)+" "+str(value.name)+"_SEC")
                # # tab like display
                ax.invert_yaxis()
            i += 1
        else:
            import seaborn as sns
            ax = fig.add_subplot(a, b, i)
            ax.set_title(str(plate.name)+" "+str(value.name))
            sns.set()
            sns.heatmap(value.array, cmap="YlGnBu")
            if sec_data:
                ax = fig.add_subplot(a, b, i+b)
                ax.set_title(str(plate.name)+" "+str(value.name)+"_SEC")
                sns.set()
                sns.heatmap(value.array_c, cmap="YlGnBu")
            i += 1

    if fpath is not None:
        plt.savefig(fpath, dpi=500)
        plt.close()
    else:
        plt.show(block=True)

def HeatMapPlates(*args, sec_data=False, fpath=None, size=3., render="matplotlib"):
    """
    Make heatmap from all replica of given plate object
    """
    import matplotlib
    import pylab as plt
    import numpy as np

    render_list = ["matplotlib", "seaborn"]
    assert render in render_list, "{0} render not available, use instead {1}".format(render, render_list)

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
    if sec_data:
        n *= 2
    a = np.floor(n**0.5).astype(int)
    b = np.ceil(1.*n/a).astype(int)
    fig = plt.figure(figsize=(size*b*1.5, size*a))
    i = 1
    
    for plate in screen:
        for key, value in plate:
            if render == "matplotlib":
                ax = fig.add_subplot(a, b, i)
                ax.pcolor(value.array, cmap=plt.cm.Reds, edgecolors='k')
                ax.set_title(str(plate.name)+" "+str(value.name))
                # # tab like display
                ax.invert_yaxis()
                if sec_data:
                    ax = fig.add_subplot(a, b, i+(n/2))
                    ax.pcolor(value.array_c, cmap=plt.cm.Reds, edgecolors='k')
                    ax.set_title(str(plate.name)+" "+str(value.name)+"_SEC")
                    # # tab like display
                    ax.invert_yaxis()
                i += 1
            else:
                import seaborn as sns
                ax = fig.add_subplot(a, b, i)
                ax.set_title(str(plate.name)+" "+str(value.name))
                sns.set()
                sns.heatmap(value.array, cmap="YlGnBu")
                if sec_data:
                    ax = fig.add_subplot(a, b, i+(n/2))
                    ax.set_title(str(plate.name)+" "+str(value.name)+"_SEC")
                    sns.set()
                    sns.heatmap(value.array_c, cmap="YlGnBu")
                i += 1
    fig.set_tight_layout(True)

    if fpath is not None:
        plt.savefig(fpath)
        plt.close()
    else:
        plt.show(block=True)

def systematic_error(obj, file_path=None, sec_data=False):
    """
    plot systematic error in cols and rows axis
    :param array: take a numpy array in input
    """
    from TransCellAssay.Core.GenericPlate import GenericPlate
    assert isinstance(obj, GenericPlate)

    if sec_data & bool(obj.array_c is not None):
        array = obj.array_c
    else:
        array = obj.array

    import numpy as np

    try:
        import matplotlib.pyplot as plt

        rowmean = np.mean(array, axis=1)
        rowstd = np.std(array, axis=1)
        colmean = np.mean(array, axis=0)
        colstd = np.std(array, axis=0)

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
        ax0.set_title('Row Mean')
        ax1.set_ylabel('Mean')
        ax1.set_title('Col Mean')

        plt.tick_params(axis="both", which="both", bottom="off", top="off",
                labelbottom="on", left="off", right="off", labelleft="on")

        if file_path is not None:
            plt.savefig(file_path)
            plt.close()
        else:
            plt.show(block=True)
    except Exception as e:
        print(e)

def boxplot_by_wells(replica, channel, file_path=None):
    """
    plot the boxplot for each well
    :param replica:
    :param channel; whiche channel to display
    """
    assert isinstance(replica, TCA.Core.Replica)
    try:
        import pandas as pd
        import matplotlib.pyplot as plt

        pd.options.display.mpl_style = 'default'
        bp = replica.df.boxplot(column=channel, by='Well')
        if file_path is not None:
            plt.savefig(file_path)
            plt.close()
        else:
            plt.show(block=True)
    except Exception as e:
        print(e)

def well_count(replica, file_path=None):
    """

    :param replica:
    :param file_path:
    :return:
    """
    assert isinstance(replica, TCA.Core.Replica)
    try:
        import pandas as pd
        import matplotlib.pyplot as plt

        pd.options.display.mpl_style = 'default'

        dfgb = replica.get_groupby_data()
        dfgb.size().plot(kind='bar')

        if file_path is not None:
            plt.savefig(file_path)
            plt.close()
        else:
            plt.show(block=True)

    except Exception as e:
        print(e)

def well_sorted(replica, well, channel, ascending=True, file_path=None):
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
        df_sorted = df.sort_values(inplace=False, axis=ascending)
        df_sorted = df_sorted.reset_index()
        df_sorted = df_sorted.drop('index', 1)
        df_sorted.plot()

        if file_path is not None:
            plt.savefig(file_path, dpi=200)
            plt.close()
        else:
            plt.show(block=True)

    except Exception as e:
        print(e)

def wells_sorted(plate, wells, channel, ascending=True, y_lim=None, file_name=None):
    """
    """
    assert isinstance(plate, TCA.Plate)
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mtick

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for well in wells:
        wellData = plate.get_raw_data(channel=channel, well=well, as_dict=True)
        for key, value in wellData.items():
            value.sort_values(inplace=True, ascending=ascending)
            perc = np.linspace(0,100,len(value))
            plt.plot(perc, value.values, label=str(key)+'_'+str(well))
    plt.legend()
    ax.set_ylabel('Well value')
    ax.set_title("Wells sorted on "+str(channel))
    if y_lim is not None:
        ax.axis([0,100, 0, y_lim])
    fmt = '%.0f%%' # Format you want the ticks, e.g. '40%'
    xticks = mtick.FormatStrFormatter(fmt)
    ax.xaxis.set_major_formatter(xticks)
    if file_name is not None:
        plt.savefig(file_name)
        plt.close()
    else:
        plt.show()

def plate_well_count(plate, file_path=None, size=3.):
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
        fig = plt.figure(figsize=(size*b*1.5, size*a))

        i = 1
        for key, value in plate:
            assert isinstance(value, TCA.Core.Replica)
            ax = fig.add_subplot(a, b, i)
            df = value.df
            df.groupby('Well').size().plot(kind='bar')
            ax.set_title(str(plate.name)+' '+str(value.name))
            i += 1
        if file_path is not None:
            plt.savefig(file_path)
            plt.close()
        else:
            plt.show(block=True)

    except Exception as e:
        print(e)

def dual_flashlight_plot(y, x, label_x='x', label_y='y', y_lim=None, x_lim=None, marker='0', color='r', file_path=None):
    """
    x and y array
    :param y: array
    :param x: array
    """
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.scatter(y.flatten(), x.flatten(), c=color, marker=marker)

    ax.set_ylabel(label_y)
    ax.set_xlabel(label_x)
    if y_lim is not None and x_lim is not None:
        ax.axis([0,x_lim, 0, y_lim])

    if file_path is not None:
        plt.savefig(file_path, dpi=200)
        plt.close()
    else:
        plt.show(block=True)

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
                    data = value.array_c.flatten()
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
            plt.close()
        else:
            plt.show(block=True)
    except Exception as e:
        print(e)

def plot_wells_distribution(plate, wells, channel, by_name=False, kind='kde', rep=None, pool=False, bins=100,
                            file_path=None):
    """
    Plot distribution of multiple well with kde or hist
    :param plate: Plate with replica
    :param wells: list of wells to plot distribution
    :param channel: which channel to plot
    :param by_name: if True the wells must be a valid genename from plate
    :param rep: if rep is provided, plot only distribution of selected wells for this one
    :param pool: if pool is True, the selected wells are pooled across replica
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
                if by_name:
                    Well = plate.platemap.search_well(Well)
                rep_series[rep] = pd.Series(plate[rep].get_rawdata(channel=channel, well=Well))
                rep_series[rep].name = str(rep)+str(Well)
            else:
                for key, value in plate.replica.items():
                    if by_name:
                        Well = plate.platemap.search_well(Well)
                    rep_series[key] = pd.Series(value.get_rawdata(channel=channel, well=Well))
                    rep_series[key].name = key+str(Well)
            # # Plotting with pandas
            if pool:
                pooled_data = pd.Series()
                for key, value in rep_series.items():
                    pooled_data = pooled_data.append(value)
                pooled_data.name = str(Well)
                if kind == 'hist':
                    pooled_data.plot(kind=kind, alpha=0.5, legend=True, bins=bins)
                else:
                    pooled_data.plot(kind=kind, alpha=0.5, legend=True)
            else:
                for key, value in rep_series.items():
                    if kind == 'hist':
                        value.plot(kind=kind, alpha=0.5, legend=True, bins=bins)
                    else:
                        value.plot(kind=kind, alpha=0.5, legend=True)
        if file_path is not None:
            plt.savefig(file_path)
            plt.close()
        else:
            plt.show(block=True)
    except Exception as e:
        print(e)

def plot_3d_cloud_point(title, x, y, z, x_label='x', y_label='y', z_label='z', size=8):
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

        fig = plt.figure(figsize=(size, size))
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

def plot_3d_per_well(replica, x, y, z, single_cell=True, skip_wells=[], size=8):
    """
    Plot in 3d raw data with choosen channels and with different color by well
    :param single_cell: plot all cell or only median
    :param replica: replica object
    :param x: x channel
    :param y: y channel
    :param z: z channel
    :param skip_wells: skip some wells if wanted
    """
    assert isinstance(replica, TCA.Core.Replica)
    try:
        import pandas as pd
        import numpy as np
        from matplotlib import pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from mpl_toolkits.mplot3d import proj3d

        wells = replica.get_unique_well()
        fig = plt.figure(figsize=(size, size))
        ax = fig.add_subplot(111, projection='3d')
        plt.rcParams['legend.fontsize'] = 10
        for well in wells:
            if well not in skip_wells :
                if single_cell:
                    ax.plot(replica.df[x][replica.df['Well'] == well].values,
                            replica.df[y][replica.df['Well'] == well].values,
                            replica.df[z][replica.df['Well'] == well].values, '.', markersize=4, alpha=0.5,
                            label=str(well))
                else:
                    ax.plot([np.median(replica.df[x][replica.df['Well'] == well].values)],
                            [np.median(replica.df[y][replica.df['Well'] == well].values)],
                            [np.median(replica.df[z][replica.df['Well'] == well].values)], '.', markersize=4, alpha=0.5,
                            label=str(well))
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_zlabel(z)

        plt.title('Raw Data point')
        ax.legend(loc='upper right')
        plt.show(block=True)
    except Exception as e:
        print(e)
