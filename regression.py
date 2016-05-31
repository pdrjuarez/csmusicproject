# Regression: Class to calculate correlations and regression coefficients
# Used primarily as a way to conceptualize running regressions 
# before implementing it in an MRJob
import math

class LinearRegression:

    def __init__(self, n, sumx, sumy, sumxx, sumyy, sumxy):
        self.n = n
        self.sumx = sumx
        self.sumy = sumy
        self.sumxx = sumxx
        self.sumyy = sumyy
        self.sumxy = sumxy

        self.beta0 = 0
        self.beta1 = 0
        self.corr = 0

        self.SE_beta0 = 0
        self.SE_beta1 = 0

        if self.calculate_corr():
            self.calculate_betas()
        else:
            print("ERROR: Could not calculate coefficients")

    def calculate_corr(self):
        '''
        Computes a basic Pearson correlation coefficient.
        Fails if the denominator would not make sense,
        or if the correlation was less than a given epsilon.
        '''
        denom = math.sqrt((self.n * self.sumxx - self.sumx**2)
                            * (self.n * self.sumyy - self.sumy**2))
        if denom < 0.0001:
            return False

        num = self.n * self.sumxy - self.sumx * self.sumy 
        self.corr = num / denom

        if abs(self.corr) < 0.0001:
            return False

        return True

    def calculate_betas(self):
        '''
        Calculates the regression coefficients.
        '''
        beta1_num = self.sumxy - self.sumx * self.sumy / self.n
        beta1_denom = self.sumxx - self.sumx**2 / self.n
        self.beta1 = beta1_num / beta1_denom

        self.beta0 = (self.sumy - self.beta1 * self.sumx) / self.n

    def fit_value(self, newx):
        '''
        Given an x value, returns the fitted y value.
        '''
        return self.beta0 + self.beta1 * newx

    def __repr__(self):
        return "SLR: b0={}, b1={}, r={}".format(
                                self.beta0, self.beta1, self.corr)


class XY:
    '''
    Given two vectors of equal length X and Y, computes and stores
    the values necessary to run a regression.
    
    Usage with LinearRegression class:
        t = LinearRegression(xy.n, xy.sumx, xy.sumy, xy.sumxx, xy.sumyy, xy.sumxy)
    '''
    def __init__(self, x, y):
        assert len(x) == len(y)
        self.n = len(x)
        self.x = x
        self.y = y
        self.sumx = 0
        self.sumy = 0
        self.sumxx = 0
        self.sumyy = 0
        self.sumxy = 0
        self.run()

    def run(self):
        self.sumx = sum(self.x)
        self.sumy = sum(self.y)
        
        # sum(x * x)
        for v in self.x:
            xx = v * v
            self.sumxx += xx
        
        # sum(y * y)
        for v in self.y:
            yy = v * v
            self.sumyy += yy

        # sum(x * y)
        for i in range(len(self.x)):
            xy = self.x[i] * self.y[i]
            self.sumxy += xy
