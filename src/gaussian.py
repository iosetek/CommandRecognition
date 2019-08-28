from scipy.stats import multivariate_normal as mvn
import random
import numpy as np

class Gaussian:
    """
    Gaussian object is simple representation of ND gauss distribution.
    """
    def __init__(self, mean, cov):
        self.__mean = mean
        self.__cov = cov
        self.__validate()
        self.__normal = mvn(mean, cov, allow_singular=True)


    def __validate(self):
        if not isinstance(self.__mean, np.ndarray) or not isinstance(self.__cov, np.ndarray):
            raise Gaussian.MeanOrCovarianceIsNotNumpyArrayException
        if len(self.__mean) == 0 or len(self.__cov) == 0:
            raise Gaussian.ZeroDimensionsException
        if len(self.__mean.shape) != 1:
            raise Gaussian.MeanMatrixIsNotSingleDimensionedException
        if len(self.__cov.shape) != 2:
            raise Gaussian.CovarianceMatrixIsNotTwoDimensional
        if self.__cov.shape[0] != self.__cov.shape[1]:
            raise Gaussian.CovarianceMatrixIsNotSquaredException
        dimensions = len(self.__cov)
        for i in range(dimensions):
            if len(self.__cov[i]) != dimensions:
                raise Gaussian.CovarianceMatrixIsNotSquaredException
        if len(self.__mean) != dimensions:
            raise Gaussian.MeanAndCovarianceHaveDifferentSizesException


    @classmethod
    def generate_random_gaussian(cls, n_dimensions):
        mean = np.array([0] * n_dimensions, dtype=float)
        sigma = np.array([[0] * n_dimensions] * n_dimensions, dtype=float)

        for i in range(n_dimensions):
            # TODO: Multivariate normal should accept 0 values, not require just a small value.
            for j in range(n_dimensions):
                sigma[i][j] = 0.001
            mean[i] = random.randint(0, 1000) / 500
            sigma[i][i] = random.randint(100, 1000) / 50

        return Gaussian(mean, sigma)


    # TODO Name it correctly
    def get_probability_for_position(self, pos):
        return self.__normal.pdf(pos)


    def get_mean(self):
        return self.__mean


    # TODO Verify this name
    def get_covariance(self):
        return self.__cov


    def is_equal_to(self, gaussian, tolerance=0.0001):
        if len(self.__mean) != len(gaussian.get_mean()):
            return False
        if len(self.__cov) != len(gaussian.get_covariance()):
            return False
        if sum(abs(self.__mean - gaussian.get_mean())) > tolerance:
            return False
        if sum(sum(abs(self.__cov - gaussian.get_covariance()))) > tolerance:
            return False

        return True

    
    class ZeroDimensionsException(Exception):
        pass


    class CovarianceMatrixIsNotTwoDimensional(Exception):
        pass


    class MeanMatrixIsNotSingleDimensionedException(Exception):
        pass


    class CovarianceMatrixIsNotSquaredException(Exception):
        pass


    class MeanAndCovarianceHaveDifferentSizesException(Exception):
        pass


    class MeanOrCovarianceIsNotNumpyArrayException(Exception):
        pass
