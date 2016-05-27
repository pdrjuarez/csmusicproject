# Regression: Class to calculate correlations and regression coefficients
#
#
import math

class LinearRegression:

    def __init__(self, n, sumx, sumy, sumxx, sumyy, sumxy):
        '''
        '''
        self.beta0 = 0
        self.beta1 = 0
        self.corr = 0
        if self.calculate_corr():
            self.calculate_betas()
        else:
            print("ERROR: Could not calculate coefficients")

    def calculate_corr(self):
        denom = math.sqrt((n * sumxx - sumx**2) * (n * sumyy - sumy**2))
        if denom < 0.0001:
            return False

        num = n * sumxy - sumx * sumy 
        self.corr = num / denom

        if abs(self.corr) < 0.0001:
            return False

        return True

    def calculate_betas(self):
        beta1_num = sumxy - sumx * sumy / n
        beta1_denom = sumxx - sumx**2 / n
        self.beta1 = beta1_num / beta1_denom

        self.beta0 = (sumy - self.beta1 * sumx) / n

