from scipy.stats import multivariate_normal as mvn
import numpy as np
import math
from bigfloat import BigFloat
import bigfloat

class DiagonalMultivariateNormal:
    def __init__(self, mean, sigma):
        self.__mean = mean
        self.__sigma = sigma
        self.__d = len(mean)
        # Used for parameter validation purpose
        mvn(mean, sigma)
    
    def pdf(self, pos):
        return self.__calculate_fraction() * self.__calculate_exp_function(pos)


    def __calculate_exp_function(self, pos):
        diffs = self.__diff_between_mean_and_pos(pos)
        out_matrix = self.__inversed_sigma_matrix_by_diffs(diffs)
        return bigfloat.exp(-0.5 * self.__diffs_by_the_result_output(diffs, out_matrix))

        

    def __inversed_sigma_matrix_by_diffs(self, diffs):
        s = self.__sigma_inversed()
        result = []
        for i in range(self.__d):
            result.append(s[i] * diffs[i])
        return result


    def __sigma_inversed(self):
        inversed = []
        for v in iter(self.__sigma):
            inversed.append(1/v)
        return inversed

    
    def __diffs_by_the_result_output(self, diffs, out_matrix):
        result = 0
        for i in range(self.__d):
            result += diffs[i] * out_matrix[i]
        return result


    def __diff_between_mean_and_pos(self, pos):
        return np.array(pos, dtype=float) - np.array(self.__mean, dtype=float)


    def __calculate_fraction(self):
        powered_pi = self.__double_pi_powered_by(self.__d)
        return BigFloat.exact('1', precision=110)/bigfloat.sqrt((powered_pi * self.__multiply_sigma()))


    def __double_pi_powered_by(self, value):
        doubled = 2 * math.pi
        result = BigFloat.exact('1', precision=110)
        for _ in range(value):
            result *= doubled
        return result


    def __multiply_sigma(self):
        result = BigFloat.exact('1', precision=110)
        for v in iter(self.__sigma):
            result *= v
        return result

    
    class NotEnoughReserveException(Exception):
        pass