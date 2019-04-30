import math

from scipy.stats import multivariate_normal as mvn

class Gaussian:
    """
    Gaussian object is simple representation of single 2D gauss distribution.
    """

    def __init__(self, pi, mi, sigma):
        self.__pi = pi
        self.__mi = mi
        self.__sigma = sigma
        self.__normal = mvn(mi, sigma)

    def compare_to_gaussian(self, other_gaussian):
        """
        Returns the difference between this and other gaussian
        passed as a parameter.
        """
        print("TODO")

    # TODO Ensure this is correct
    # TODO Name it correctly
    def get_probability_for_position(self, x1, x2):
        return self.__pi * self.__normal.pdf([x1, x2])

    def get_top_position(self):
        return self.__mi

    def get_variances(self):
        return self.__sigma

    def get_pi(self):
        return self.__pi
    
