import math

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
        # TODO Finish this class

    def compare_to_gaussian(self, other_gaussian):
        """
        Returns the difference between this and other gaussian
        passed as a parameter.
        """
        print("TODO")

    # TODO Name it correctly
    def get_probability_for_position(self, x1, x2):
        # TODO Notify that this function won't necessary return value from range 0 to 1 
        a = (1 / math.sqrt(self.__sigmaX * self.__sigmaY))
        b = self.__sigmaX * (x1 - self.__miX) * (x1 - self.__miX)
        c = self.__sigmaY * (x2 - self.__miY) * (x2 - self.__miY)
        return const_value * a * math.exp((-1/2) * (b + c))
    
