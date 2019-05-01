import math
import numpy as np
import random

from src.gaussian import Gaussian

def estimate_n_gaussians_from_mfcc_data(mfcc_data, n_gaussians, n_iterations=15):
    """
    Uses EM algorithm to estimate gaussian distributions for
    passed mfcc data.\n
    n_iterations - number of iterations. Usually 15 iterations are
    enough, any next iteration slightly changes gaussians estimated
    earlier.
    """
    gaussians = __pick_random_gaussians(mfcc_data, n_gaussians)
    
    for _ in range(n_iterations):
        gaussians = single_em_iteration(gaussians, mfcc_data)

    return gaussians


def __pick_random_gaussians(mfcc_data, n_gaussians):
    gaussians = []

    frames_count = len(mfcc_data)
    coefficients_count = len(mfcc_data[0])

    ratio_mean_frames = frames_count / n_gaussians
    ratio_mean_coefficients = coefficients_count / n_gaussians

    pi = 1 / n_gaussians
    sigma = np.array([[2, 0], [0, 2]], dtype=float)

    for i in range(n_gaussians):
        # TODO Verify if this is correct
        mean = np.array([ratio_mean_frames * i, ratio_mean_coefficients * i], dtype=float)
        gaussians.append(Gaussian(pi, mean, sigma))

    return gaussians


def single_em_iteration(gaussians, mfcc_data):
    estimations = __get_estimations(mfcc_data, gaussians)
    for i in range(len(gaussians)):
        pi = __get_pi_of_mfcc_data(mfcc_data, estimations[i])
        mean = __get_mean_of_mfcc_data(mfcc_data, estimations[i])
        sigma = __get_sigma_of_mfcc_data(mfcc_data, estimations[i], mean)
        gaussians[i] = Gaussian(pi, mean, sigma)
    return gaussians


def __get_sum_of_mfcc_data(mfcc_data):
    return sum(sum(mfcc_data))


def __get_pi_of_mfcc_data(mfcc_data, estimations):
    a = __get_sum_of_estimations(mfcc_data, estimations)
    b = __get_sum_of_mfcc_data(mfcc_data)
    return (a / b)


def __get_sum_of_estimations(mfcc_data, estimations):
    result = 0
    frames_count = len(mfcc_data)
    coefficients_count = len(mfcc_data[0])
    for i in range(frames_count):
        for j in range(coefficients_count):
            result += mfcc_data[i][j] * estimations[i][j]
    return result


def __get_mean_of_mfcc_data(mfcc_data, estimations):
    # TODO Check order X/Y
    frames_count = len(mfcc_data)
    coefficients_count = len(mfcc_data[0])
    mean = np.zeros((2))
    for i in range(frames_count):
        for j in range(coefficients_count):
            # TODO Ensure if x, y should not be swapped
            mean += mfcc_data[i][j] * estimations[i][j] * np.array([i, j])
    return (mean / __get_sum_of_estimations(mfcc_data, estimations))


def __get_sigma_of_mfcc_data(mfcc_data, estimations, mean):
    # TODO This method is designed mostly for 2D data so maybe it should
    # be explicit.
    # TODO Check order X/Y
    number_of_dimensions = 2
    sigma = np.zeros((number_of_dimensions, number_of_dimensions))
    frames_count = len(mfcc_data)
    coefficients_count = len(mfcc_data[0])
    for i in range(frames_count):
        for j in range(coefficients_count):
            # TODO Check if this reshape is necessary
            # TODO Check if i/j has the right order
            ys = np.reshape(np.array([i, j]) - mean, (2,1))
            sigma += mfcc_data[i][j] * estimations[i, j] * np.dot(ys, ys.T)

    return (sigma / __get_sum_of_estimations(mfcc_data, estimations))


def __get_estimations(mfcc_data, gaussians):
    """
    E step.
    """
    # TODO Check if height/width order is correct
    # TODO Keep one style: height/width or data/coefficients
    frames_count = len(mfcc_data)
    coefficients_count = len(mfcc_data[0])
    estimations = np.zeros((len(gaussians), frames_count, coefficients_count))
    summed_estimations = np.zeros((frames_count, coefficients_count))
    for i in range(len(gaussians)):
        for j in range(frames_count):
            for k in range(coefficients_count):
                estimation = gaussians[i].get_probability_for_position(j, k)
                estimations[i][j][k] = estimation
                summed_estimations[j][k] += estimation

    for i in range(len(gaussians)):
        estimations[i] /= summed_estimations
    return estimations


