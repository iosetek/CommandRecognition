from scipy.stats import multivariate_normal as mvn
import random

class Gaussian:
    """
    Gaussian object is simple representation of ND gauss distribution.
    """
    def __init__(self, mean, cov):
        self.__mean = mean
        self.__cov = cov
        self.__normal = mvn(mean, cov)


    @classmethod
    def generate_random_gaussian(cls, n_dimensions):
        mean = [0] * n_dimensions
        sigma = [[0] * n_dimensions] * n_dimensions

        for i in range(n_dimensions):
            mean[i] = random.randint(0, 1000) / 500
            sigma[i][i] = random.randint(100, 1000) / 50

        return Gaussian(mean, sigma)


    # TODO Name it correctly
    def get_probability_for_position(self, pos):
        return self.__normal.pdf(pos)


    def get_mean(self):
        return self.__mean


    def get_covariance(self):
        return self.__cov