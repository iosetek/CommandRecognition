import numpy as np

from src.gaussian import Gaussian
from src.mfcc import MFCCParser

# TODO Use Phonem length in methods or remove this variable.

class EM:
    """
    Class EM represents EM algorithm designed for extracting
    gauss distributions for set of MFCC data.\n
    Parameters:\n
    
    phonem_length - length of single phonem class represented as
    number of MFCC vectors that will be used to describe it.\n
    
    gaussian_models - number of gauss distributions that will be
    resolved from single phonem MFCC data to be representantive
    for this phonem class.
    """

    def __init__(self, phonem_length, gaussian_models):
        self.__phonem_length = phonem_length
        self.__gaussian_models = gaussian_models


    #TODO Set iteration number to 15
    def estimate_gaussians_from_mfcc_data(self, mfcc_data, n_iterations=15):
        """
        Uses EM algorithm to estimate gaussian distributions for
        passed mfcc data.\n
        n_iterations - number of iterations. Usually 15 iterations are
        enough, any next iteration slightly changes gaussians estimated
        earlier.
        """
        gaussians = self.__pick_random_gaussians()
        data = MFCCParser.enlarge_each_cell_to_be_positive(mfcc_data)

        # TODO Verify if data should be intiger and if do then set data here
        
        for _ in range(n_iterations):
            gaussians = self.single_em_iteration(gaussians, data)

        return gaussians

    # TODO Handle it properly!
    def __pick_random_gaussians(self):
        gaussians = []
        # for i in range(self.__gaussian_models):

        return [Gaussian(0.3, [0, 1], [[2, 0],[0, 2]]),
        Gaussian(0.4, [3, 4], [[1, 0],[0, 3]]),
        Gaussian(0.3, [5, 5], [[4, 0],[0, 2.5]])]


    def single_em_iteration(self, gaussians, mfcc_data):
        estimations = EM.__get_estimations(mfcc_data, gaussians)

        for i in range(len(gaussians)):
            #TODO Fix pi estimation
            pi = EM.__get_pi_of_mfcc_data(mfcc_data, estimations[i])
            mean = EM.__get_mean_of_mfcc_data(mfcc_data, estimations[i])
            sigma = EM.__get_sigma_of_mfcc_data(mfcc_data, estimations[i], mean)
            gaussians[i] = Gaussian(pi, mean, sigma)
        return gaussians


    @staticmethod
    def __get_sum_of_mfcc_data(mfcc_data):
        return sum(sum(mfcc_data))

    @staticmethod
    def __get_pi_of_mfcc_data(mfcc_data, estimations):
        a = EM.__get_sum_of_estimations(mfcc_data, estimations)
        b = EM.__get_sum_of_mfcc_data(mfcc_data)
        return (a / b)

    @staticmethod
    def __get_sum_of_estimations(mfcc_data, estimations):
        result = 0
        number_of_coefficients = len(mfcc_data)
        number_of_data = len(mfcc_data[0])
        for x in range(number_of_data):
            for y in range(number_of_coefficients):
                result += mfcc_data[y][x] * estimations[y][x]
        return result


    @staticmethod
    def __get_mean_of_mfcc_data(mfcc_data, estimations):
        # TODO Check order X/Y
        number_of_coefficients = len(mfcc_data)
        number_of_data = len(mfcc_data[0])
        mean = np.zeros((2))
        for x in range(number_of_data):
            for y in range(number_of_coefficients):
                # TODO Ensure if x, y should not be swapped
                mean += mfcc_data[y][x] * estimations[y][x] * np.array([y, x])
        # TODO Ensure it should not be divided by the sum of mfcc data multiplied by
        # each position
        return (mean / EM.__get_sum_of_estimations(mfcc_data, estimations))

    @staticmethod
    def __get_sigma_of_mfcc_data(mfcc_data, estimations, mean):
        # TODO This method is designed mostly for 2D data so maybe it should
        # be explicit.
        # TODO Check order X/Y
        number_of_dimensions = 2
        sigma = np.zeros((number_of_dimensions, number_of_dimensions))
        number_of_coefficients = len(mfcc_data)
        number_of_data = len(mfcc_data[0])
        for x in range(number_of_data):
            for y in range(number_of_coefficients):
                # TODO Check if this reshape is necessary
                # TODO Check if i/j has the right order
                ys = np.reshape(np.array([y, x]) - mean, (2,1))
                sigma += mfcc_data[y][x] * estimations[y, x] * np.dot(ys, ys.T)

        return (sigma / EM.__get_sum_of_estimations(mfcc_data, estimations))

    @staticmethod
    def __get_estimations(mfcc_data, gaussians):
        """
        E step.
        """
        # TODO Check if height/width order is correct
        # TODO Keep one style: height/width or data/coefficients
        height, width = mfcc_data.shape
        estimations = np.zeros((len(gaussians), height, width))
        summed_estimations = np.zeros((height, width))
        for i in range(len(gaussians)):
            for y in range(height):
                for x in range(width):
                    estimation = gaussians[i].get_probability_for_position(y, x)
                    estimations[i][y][x] = estimation
                    summed_estimations[y][x] += estimation

        # THIS SUM IS WRONG. HANDLE IT PROPERLY. YOU NEED TO DIVIDE EACH ESTIMATION BY THE SUM OF ESTIMATIONS
        # FROM EACH GAUSSIAN
        for i in range(len(gaussians)):
            estimations[i] /= summed_estimations
        return estimations


