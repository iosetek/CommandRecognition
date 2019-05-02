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

    def is_equal_with_gaussian(self, gaussian):
        """
        Returns true if the following gaussian has the same
        pi, mean and variance as the other 2D gaussian.
        """

        if not math.isclose(self.__pi, gaussian.get_pi(), abs_tol=0.00001):
            return False
        for i in range(2):
            if not math.isclose(self.__mi[i], gaussian.get_top_position()[i], abs_tol=0.00001):
                return False
        for i in range(2):
            for j in range(2):
                if not math.isclose(self.__sigma[i][j], gaussian.get_variances()[i][j], abs_tol=0.00001):
                    return False
        return True