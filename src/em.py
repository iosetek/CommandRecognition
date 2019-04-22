from src.mfcc import MFCCParser
from src.gaussian import Gaussian
import statistics
import numpy as np
from statsmodels.stats.weightstats import DescrStatsW
from scipy.stats import multivariate_normal as mvn

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
    def estimate_gaussians_from_mfcc_data(self, mfcc_data, n_iterations=5):
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
        
        # TODO Remove indo variable
        for indo in range(n_iterations):
            gaussians = self.__single_em_iteration(gaussians, data, indo)

        return gaussians

    # TODO Investigate if using DescrStatsW is not an overkill for those cases
    # TODO Investigate if data should not be intiger to make calculations easier
    def __get_best_matching_gaussian_for_data(self, mfcc_data):
        # TODO: Ensure those functions work properly

        # TODO: Check if those sum vectors should not be calculated with multiplying them by their index
        x_data = EM.__get_vector_of_horizontal_sums(mfcc_data)
        y_data = EM.__get_vector_of_vertical_sums(mfcc_data)

        x_data_stats = DescrStatsW(range(len(x_data)), weights=x_data, ddof=0)
        y_data_stats = DescrStatsW(range(len(y_data)), weights=y_data, ddof=0)

        return Gaussian(x_data_stats.mean, y_data_stats.mean, x_data_stats.var, y_data_stats.var)

    # # TODO Ensure int values are not required



    # TODO Handle it properly!
    def __pick_random_gaussians(self):
        print("TODO")
        return [Gaussian(0, 0, 2, 2), Gaussian(0, 8, 2, 2), Gaussian(8, 0, 2, 2)]


    # TODO Remove test parameter (indo)
    def __single_em_iteration(self, gaussians, mfcc_data, indo):
        data_per_gaussian = self.__split_mfcc_data_depending_on_gaussians(gaussians, mfcc_data, indo)
        print("First gaussian: %s, %s and variances " % (gaussians[0].get_top_position()), (gaussians[0].get_variances()))
        print("Second gaussian: %s, %s and variances " % (gaussians[1].get_top_position(), gaussians[1].get_variances()))
        print("Third gaussian: %s, %s and variances \n\n" % (gaussians[2].get_top_position(), gaussians[2].get_variances()))
        for i in range(len(gaussians)):
            gaussians[i] = self.__get_best_matching_gaussian_for_data(data_per_gaussian[i])
        return gaussians


    # TODO Remove test variable indo
    def __split_mfcc_data_depending_on_gaussians(self, gaussians, mfcc_data, indo):
        """
        It returns an array of two-dimensional arrays. Each of them is a representation
        of mfcc data that belongs to specific gaussian. For example for 3 gaussians
        this method will return 3 two-dimensional arrays. First will contain mfcc data
        that fits the first gaussian, second will contain mfcc data that fits second
        gaussian etc.
        """
        if len(mfcc_data) == 0:
            raise ValueError
        datas = []
        for _ in range(self.__gaussian_models):
            datas.append(np.array([[0] * len(mfcc_data[0])]*len(mfcc_data), np.float) * self.__gaussian_models)
            
        for row_id, row in enumerate(mfcc_data):
            for cell_id, cell in enumerate(row):
                values = [0] * len(gaussians)
                for gaussian_id, gaussian in enumerate(gaussians):
                    values[gaussian_id] = gaussian.get_probability_for_position(row_id, cell_id)
                if indo == 2:
                    print("values: %s" % values)
                total_sum = sum(values)

                datas[values.index(max(values))][row_id][cell_id] = cell * max(values)
                # for gaussian_id in range(len(gaussians)):
                #     # TODO Take a look at this method once again :/
                #     print("Counted: %s" % values[gaussian_id])
                #     datas[gaussian_id][row_id][cell_id] = (values[gaussian_id]*(values[gaussian_id]/total_sum))*cell
                #     print("Normalized: %s" % (values[gaussian_id]*(values[gaussian_id]/total_sum)))
        print(datas[0])
        print(datas[1])
        print(datas[2])
        return datas


    # TODO Those methods can do that at the same time so it would take only one
    # check for entire array.

    # TODO Find better name for this method!
    @staticmethod
    def __get_vector_of_horizontal_sums(mfcc_data):
        """
        It returns vector filled up with summed up colums from
        two-dimensional array. 
        """
        result = [0] * len(mfcc_data[0])
        for row in mfcc_data:
            for index, cell in enumerate(row):
                result[index] += cell
        return result


    # TODO Find better name for this method!
    @staticmethod
    def __get_vector_of_vertical_sums(mfcc_data):
        """
        It returns vector filled up with summed up rows from
        two-dimensional array. 
        """
        result = []
        for row in mfcc_data:
            result.append(sum(row))
        return result

    @staticmethod
    def __get_sum_of_mfcc_data(mfcc_data):
        return sum(sum(mfcc_data,[]))

    @staticmethod
    def __get_pi_of_mfcc_data(mfcc_data, estimations):
        a = EM.__get_sum_of_estimations(mfcc_data, estimations)
        b = EM.__get_sum_of_mfcc_data(mfcc_data)
        return (a / b)

    @staticmethod
    def __get_sum_of_estimations(mfcc_data, estimations):
        result = 0
        number_of_data = len(mfcc_data)
        number_of_coefficients = len(mfcc_data[0])
        for i in range(number_of_data):
            for j in range(number_of_coefficients):
                result += mfcc_data[i][j] * estimations[i][j]
        return result


    @staticmethod
    def __get_mean_of_mfcc_data(mfcc_data, estimations):
        # TODO Check order X/Y
        number_of_data = len(mfcc_data)
        number_of_coefficients = len(mfcc_data[0])
        mean = np.zeros((2))
        for i in range(number_of_data):
            for j in range(number_of_coefficients):
                # TODO Ensure if i, j should not be swapped
                mean += mfcc_data[i][j] * estimations[i][j] * np.array([i, j])
        # TODO Ensure it should not be divided by the sum of mfcc data multiplied by
        # each position
        return (mean / EM.__get_sum_of_estimations(mfcc_data, estimations))

    @staticmethod
    def __get_sigma(mfcc_data, estimations, mean):
        # TODO This method is designed mostly for 2D data so maybe it should
        # be explicit.
        # TODO Check order X/Y
        number_of_dimensions = 2
        sigma = np.zeros((number_of_dimensions, number_of_dimensions))
        number_of_data = len(mfcc_data)
        number_of_coefficients = len(mfcc_data[0])
        for i in range(number_of_data):
            for j in range(number_of_coefficients):
                # TODO Check if this reshape is necessary
                # TODO Check if i/j has the right order
                ys = np.reshape(np.array([i, j]) - mean, (2,1))
                sigma += mfcc_data[i][j] * estimations[i, j] * np.dot(ys, ys.T)

        return (sigma / EM.__get_sum_of_estimations(mfcc_data, estimations))

    @staticmethod
    def __get_estimations(mfcc_data, gaussian):
        # TODO Check if height/width order is correct
        # TODO Keep one style: height/width or data/coefficients
        height, width = mfcc_data.shape
        estimations = np.zeros((height, width))
        for y in range(height):
            for x in range(width):
                estimations[y][x] = gaussian.get_probability_for_position(x, y)
        return estimations

