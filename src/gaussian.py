from src.diagonal_multivariate import DiagonalMultivariateNormal
import random
import numpy as np
from bigfloat import BigFloat

class Gaussian:
    """
    Gaussian object is simple representation of ND gauss distribution.
    """
    def __init__(self, mean, cov):
        self.__mean = mean
        self.__cov = cov
        self.__validate()
        self.__g = DiagonalMultivariateNormal(mean, cov)


    def __validate(self):
        if not isinstance(self.__mean, np.ndarray) or not isinstance(self.__cov, np.ndarray):
            raise Gaussian.MeanOrCovarianceIsNotNumpyArrayException
        if len(self.__mean) == 0 or len(self.__cov) == 0:
            raise Gaussian.ZeroDimensionsException
        if len(self.__mean.shape) != 1:
            raise Gaussian.MeanMatrixIsNotSingleDimensionedException
        if len(self.__cov.shape) != 1:
            raise Gaussian.CovarianceMatrixIsNotDimensionedException
        dimensions = len(self.__cov)
        if len(self.__mean) != dimensions:
            raise Gaussian.MeanAndCovarianceHaveDifferentSizesException


    @classmethod
    def generate_random_gaussian(cls, n_dimensions, one_vector):
        mean = np.array([BigFloat.exact("0", precision=110)] * n_dimensions)
        sigma = np.array([BigFloat.exact("0", precision=110)] * n_dimensions)

        for i in range(n_dimensions):
            # TODO: Multivariate normal should accept 0 values, not require just a small value.
            mean[i] = one_vector.component(i) + random.randint(-100, 100) / 50
            # sigma[i][i] = random.randint(100, 1000) / 0.5
            sigma[i] = 3e1

        return Gaussian(mean, sigma)


    # TODO Name it correctly
    def get_probability_for_position(self, pos):
        return self.__g.pdf(pos)


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
        if sum(abs(self.__cov - gaussian.get_covariance())) > tolerance:
            return False

        return True


    def to_json_object(self):
        return {
            Gaussian.__MEAN: self.__list_to_json_list(self.__mean),
            Gaussian.__SIGMA: self.__list_to_json_list(self.__cov)
        }


    @classmethod
    def from_json_obj(cls, obj):
        return Gaussian(
            cls.__json_list_to_numpy_list(obj[Gaussian.__MEAN]),
            cls.__json_list_to_numpy_list(obj[Gaussian.__SIGMA])
        )
        

    def __list_to_json_list(self, oldList):
        jsonList = []
        for v in iter(oldList):
            jsonList.append({
                Gaussian.__VALUE: v.__str__(),
                Gaussian.__PRECISION: v.precision()
            })
        return jsonList


    @classmethod
    def __json_list_to_numpy_list(self, jsonList):
        newList = []
        for v in iter(jsonList):
            newList.append(BigFloat.exact(v[Gaussian.__VALUE], precision=v[Gaussian.__PRECISION]))
        return np.array(newList)

    
    class ZeroDimensionsException(Exception):
        pass


    class CovarianceMatrixIsNotDimensionedException(Exception):
        pass


    class MeanMatrixIsNotSingleDimensionedException(Exception):
        pass


    class CovarianceMatrixIsNotSquaredException(Exception):
        pass


    class MeanAndCovarianceHaveDifferentSizesException(Exception):
        pass


    class MeanOrCovarianceIsNotNumpyArrayException(Exception):
        pass


    __MEAN = "mean"
    __SIGMA = "sigma"
    __PRECISION = "precision"
    __VALUE = "value"