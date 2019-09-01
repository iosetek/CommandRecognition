from scipy.stats import multivariate_normal as mvn
import numpy as np
import math

class DiagonalMultivariateNormal:
    def __init__(self, mean, sigma):
        self.__mean = mean
        self.__sigma = sigma
        self.__d = len(mean)
        # Used for parameter validation purpose
        mvn(mean, sigma)
    
    def pdf(self, pos, reserve=0):
        return self.__calculate_fraction(reserve) * self.__calculate_exp_function(pos)


    def __calculate_exp_function(self, pos):
        diffs = self.__diff_between_mean_and_pos(pos)
        out_matrix = self.__inversed_sigma_matrix_by_diffs(diffs)
        return math.exp(-0.5 * self.__diffs_by_the_result_output(diffs, out_matrix))

        

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


    def __calculate_fraction(self, reserve):
        # This is so user could set reserve for actual 10^x
        reserve *= 2
        (powered_pi, reserve) = self.__double_pi_powered_by(self.__d, reserve)
        return (10 ** (reserve/2))/math.sqrt((powered_pi * self.__multiply_sigma()))


    def __double_pi_powered_by(self, value, reserve):
        doubled = 2 * math.pi
        result = 1.0
        for _ in range(value):
            okay = False
            while not okay:
                old_result = result
                result *= doubled
                if result == float("inf"):
                    result = old_result / (10**4)
                    reserve -= 4
                else:
                    okay = True
        return (result, reserve)


    def __multiply_sigma(self):
        result = 1
        for v in iter(self.__sigma):
            result *= v
        return result

    
    class NotEnoughReserveException(Exception):
        pass