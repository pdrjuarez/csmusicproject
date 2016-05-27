# Regression: Class to calculate correlations and regression coefficients
#
#
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
        if self.calculate_corr():
            self.calculate_betas()
        else:
            print("ERROR: Could not calculate coefficients")

    def calculate_corr(self):
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
        beta1_num = self.sumxy - self.sumx * self.sumy / self.n
        beta1_denom = self.sumxx - self.sumx**2 / self.n
        self.beta1 = beta1_num / beta1_denom

        self.beta0 = (self.sumy - self.beta1 * self.sumx) / self.n

    def fit_value(self, newx):
        return self.beta0 + self.beta1 * newx

    def __repr__(self):
        return "SLR: b0={}, b1={}, r={}".format(
                                self.beta0, self.beta1, self.corr)


class XY:
    '''
    This is just for very basic testing purposes. 
    Ideally, MRJob will give us the information we want.

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

        for v in self.x:
            xx = v * v
            self.sumxx += xx

        for v in self.y:
            yy = v * v
            self.sumyy += yy

        for i in range(len(self.x)):
            xy = self.x[i] * self.y[i]
            self.sumxy += xy