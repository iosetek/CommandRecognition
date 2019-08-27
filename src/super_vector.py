import numpy as np
import math

class SuperVector:
    def __init__(self, data):
        """
        Creates instance of SuperVector from 1D array.
        """
        self.__data = np.array(data, dtype=float)
        self.__length = len(self.__data)


    @classmethod
    def init_from_mfcc(cls, mfcc):
        """
        Creates instance of SuperVector from 2D array.
        """
        array1d = []
        data = mfcc.get_data()
        width = len(data)
        height = len(data[0])
        for i in range(width):
            for j in range(height):
                array1d.append(data[i][j])
        return SuperVector(array1d)
    

    def dimensions(self):
        return len(self.__data)


    def component(self, dimension_id):
        return self.__data[dimension_id]


    def matrix(self):
        return self.__data 


    def is_equal_to(self, vector, tolerance=0.0001):
        """
        Returns true if SuperVector is the same as another vector.
        """
        if self.dimensions() != vector.dimensions():
            return False
        for i in range(self.dimensions()):
            if not math.isclose(self.component(i), vector.component(i), abs_tol=tolerance):
                return False
        return True
