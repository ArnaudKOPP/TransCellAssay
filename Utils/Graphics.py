__author__ = 'Arnaud KOPP'
"""
Method for making graphics of plate
"""

def plotHist3D_Plate(array):
    '''
    Make a 3d histogramme plot of matrix representing plate, give an array(in matrix form) of value (whatever you want)

    Source : http://matplotlib.org/examples/mplot3d/hist3d_demo.html
    alt : https://qutip.googlecode.com/svn/doc/1.1.3/html/examples/examples-3d-histogram.html

    :param array:
    :return:
    '''
    try:
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        import numpy as np

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x, y = np.random.rand(2, 100) * 4
        hist, xedges, yedges = np.histogram2d(x, y, bins=4)

        elements = (len(xedges) - 1) * (len(yedges) - 1)
        xpos, ypos = np.meshgrid(xedges[:-1]+0.25, yedges[:-1]+0.25)

        xpos = xpos.flatten()
        ypos = ypos.flatten()
        zpos = np.zeros(elements)
        dx = 0.5 * np.ones_like(zpos)
        dy = dx.copy()
        dz = hist.flatten()

        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')

        plt.show()
    except Exception as e:
        print(e)

def plotSurf3D_Plate(array):
    '''
    Make a 3d surface plot  of matrix representing plate, give an array(in matrix form) of value (whatever you want)

    Source : http://matplotlib.org/examples/mplot3d/surface3d_demo.html

    :param array:
    :return:
    '''
    try:
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import cm
        from matplotlib.ticker import LinearLocator, FormatStrFormatter
        import matplotlib.pyplot as plt
        import numpy as np

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X**2 + Y**2)
        Z = np.sin(R)
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                linewidth=0, antialiased=False)
        ax.set_zlim(-1.01, 1.01)

        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.show()
    except Exception as e:
        print(e)


def plotPlateValue(dataFrame):
    '''
    Plot all value of plate (replicat here)
    :param dataFrame:
    :return:
    '''
    try:
        return 0
    except Exception as e:
        print(e)