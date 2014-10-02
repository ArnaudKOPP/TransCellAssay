__author__ = 'Arnaud KOPP'

### Locally weighted regression

import numpy as np
import scipy as sp
import pylab as pl


class locpoly(object):
    ''' Locally weighted regression implementation '''

    def __init__(self, bandwidth, degree):
        '''
        degree = 0 or 1 , in case of 0 model becomes just standard Nadaraya-Watson
        kernel regression, in case of 1 it is local linear regression
        '''
        self.band = bandwidth
        self.degree = degree


    def fit(self, X, y):
        self.X = X
        self.y = y
        self.estimates = []
        self.newdata = []

    def predict(self, X_0):

        def predict_point_loc_linear(x, X = self.X[:], y = self.y[:]):
            '''
            locally weighted regression of degree 1
            '''
            ## calculate distance from x to all points in X
            eucl_dist = np.array([ sp.spatial.distance.euclidean(X[i],x) for i in  range(np.shape(X)[0])])
            ## calculate weighting
            w_vector = [np.exp(-float(d)/(2*self.band**2)) for d in eucl_dist]
            W = np.eye(len(w_vector))
            for i in range(len(w_vector)):
                W[i,i] = w_vector[i]
            ## add bias term to X
            if len(np.shape(X))==1:
                cols = 2
                X_transfer = np.ones((np.shape(X)[0],1))
                X_transfer[:,0] = X
            else:
                cols = np.shape(X)[1]+1
                X_transfer = X
            X_new = np.ones( ( np.shape(X)[0], cols ) )
            X_new[:,1:] = X_transfer
            X = X_new
            ## calculate coefficients
            beta_part_one = np.linalg.inv(np.dot( np.dot( np.transpose(X), W ), X))
            beta_part_two = np.dot(np.dot( np.transpose(X), W), y)
            B = np.dot(beta_part_one, beta_part_two)
            ## estimate y at x
            x_bias = np.ones((1,cols))
            x_bias[:,1:] = x
            y_estimated = np.dot(x_bias,B)
            return y_estimated

        def predict_Nadaraya_Watson(x, X = self.X[:], y = self.y[:]):
            '''
            Nadaraya-Watson kernel regression
            '''
            ## calculate distance from x to all points in X
            print("entered here")
            eucl_dist = np.array([ sp.spatial.distance.euclidean(X[i],x) for i in  range(np.shape(X)[0])])
            print(eucl_dist)
            ## calculate weighting
            w_vector = np.array([np.exp(-float(d)/(2*self.band**2)) for d in eucl_dist])
            w = [ float(w_el)/np.sum(w_vector) for w_el in w_vector]
            ## for kernel regression estimate is just weighted sum of tragets
            y_estimated = np.sum(np.array( [y[i]*w[i] for i in range(len(y))] ))
            return y_estimated

        if self.degree == 1:
            ## locally weighted linear regression
            estimates = [ predict_point_loc_linear(X_0[i]) for i in range(np.shape(X_0)[0]) ]

        if self.degree == 0:
            ## Nadaraya - Watson kernel regression
            print(range(np.shape(X_0)[0]))
            estimates = [predict_Nadaraya_Watson(X_0[i]) for i in range(np.shape(X_0)[0]) ]

        self.newdata = X_0
        self.estimates = estimates

#if __name__=="__main__":
#    # create locpoly object
#    loess = locpoly(0.5, 1)
#    # Synthetic data
#    X = np.linspace(0,10,100)
#    y = np.random.randn(100) + np.sin(X)
#    # fit data
#    loess.fit(X,y)
#    loess.predict(X)
#    pl.figure(1)
#    pl.plot(X, loess.estimates, 'b-')
#    pl.plot(X, y, 'r+')
#    pl.show()