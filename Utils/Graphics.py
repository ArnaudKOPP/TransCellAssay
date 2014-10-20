__author__ = 'Arnaud KOPP'
"""
Method for making graphics of plate
"""


def plotHist3D_Plate(array):
    '''
    Make a 3d histogramme plot of matrix representing plate, give an array(in matrix form) of value (whatever you want)
    :param array: numpy array
    :return:show 3d plot
    '''
    try:
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


def plotSurf3D_Plate(array):
    '''
    Make a 3d surface plot  of matrix representing plate, give an array(in matrix form) of value (whatever you want)
    :param array:
    :return:
    '''
    try:
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import cm
        import matplotlib.pyplot as plt
        import numpy as np

        fig = plt.figure()
        X = np.arange(array.shape[1])
        Y = np.arange(array.shape[0])
        X, Y = np.meshgrid(X, Y)
        Z = array
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='hot', linewidth=0, antialiased=False)
        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.show()

    except Exception as e:
        print(e)


def PlateHeatmap(array):
    '''
    Plot all value of plate (replicat here)
    :param dataFrame:
    :return:
    '''
    try:
        import matplotlib
        import pylab
        import numpy as np

        # Create new colormap, with white for zero
        #(can also take RGB values, like (255,255,255):
        colors = [('white')] + [(pylab.cm.jet(i)) for i in range(1, 256)]
        new_map = matplotlib.colors.LinearSegmentedColormap.from_list('new_map', colors, N=256)

        pylab.pcolor(array, cmap=new_map)
        pylab.colorbar()
        pylab.show()
    except Exception as e:
        print(e)


def SystematicError(array):
    '''
    plot systematic error in cols and rows axis
    :param array: take a numpy array in input
    :return:
    '''
    try:
        import matplotlib.pyplot as plt
        import numpy as np

        rowMean = []
        rowStd = []
        colMean = []
        colStd = []
        if isinstance(array, np.ndarray):
            for row in range(array.shape[0]):
                rowMean.append(np.mean(array[row, :]))
                rowStd.append(np.std(array[row, :]))
            for col in range(array.shape[1]):
                colMean.append(np.mean(array[:, col]))
                colStd.append(np.std(array[:, col]))

            fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(10, 5))

            Row = np.arange(array.shape[0])
            Col = np.arange(array.shape[1])
            ax0.bar(Row, rowMean, color='r', yerr=rowStd)
            ax1.bar(Col, colMean, color='r', yerr=colStd)

            ax0.set_ylabel('Mean')
            ax0.set_title('Mean by row')
            ax1.set_ylabel('Mean')
            ax1.set_title('Mean by Col')

            plt.show()
        else:
            raise TypeError
    except Exception as e:
        print(e)


def boxplotByWell(dataframe, feature):
    '''
    plot the boxplot for each well
    :param dataframe:
    :param feature; whiche feature to display
    :return:
    '''
    try:
        import pandas as pd
        import matplotlib.pyplot as plt

        if isinstance(dataframe, pd.DataFrame):
            bp = dataframe.boxplot(column=feature, by='Well')
            plt.show()
        else:
            raise TypeError
    except Exception as e:
        print(e)