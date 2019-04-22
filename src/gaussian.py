import math
from scipy.stats import multivariate_normal as mvn

const_value = 1 / (2 * math.pi)

class Gaussian:
    """
    Gaussian object is simple representation of single 2D gauss distribution.
    """

    def __init__(self, miX, miY, sigmaX, sigmaY):
        self.__miX = miX
        self.__miY = miY
        self.__sigmaX = sigmaX
        self.__sigmaY = sigmaY
        self.__power = self.__extract_power()

        self.__normal = mvn([miX, miY], [[sigmaX, 0],[0, sigmaY]])
        # TODO Finish this class

    def compare_to_gaussian(self, other_gaussian):
        """
        Returns the difference between this and other gaussian
        passed as a parameter.
        """
        print("TODO")

    def __extract_power(self):
        # TODO Notify that this function won't necessary return value from range 0 to 1 
        a = (1 / math.sqrt(self.__sigmaX * self.__sigmaY))
        return 1/(const_value * a)

    # TODO Verify if method with power variable is valid
    # TODO Name it correctly
    def get_probability_for_position(self, x1, x2):
        return self.__normal.pdf([x1, x2])
        
        
        # # TODO Notify that this function won't necessary return value from range 0 to 1 
        # a = (1 / math.sqrt(self.__sigmaX * self.__sigmaY))
        # b = self.__sigmaX * (x1 - self.__miX) * (x1 - self.__miX)
        # c = self.__sigmaY * (x2 - self.__miY) * (x2 - self.__miY)
        # return const_value * a * math.exp((-1/2) * (b + c))
        # # return const_value * a * math.exp((-1/2) * (b + c)) * self.__power

    def get_top_position(self):
        return self.__miX, self.__miY

    def get_variances(self):
        return self.__sigmaX, self.__sigmaY
    
