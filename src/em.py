import math
import numpy as np
import random
import statistics
from src.gaussian import Gaussian
from src.super_vector import SuperVector

class DifferentNumberOfDimensionsException(Exception):
    pass

class NoSuperVectorsException(Exception):
    pass

class NotEnoughSuperVectorsException(Exception):
    pass

class NoVarianceException(Exception):
    pass


def estimate_n_gaussians(svectors, n_gaussians, iterations, em_reserve=0):
    __validate_vectors(svectors)

    gaussians = __generate_random_gaussians(n_gaussians, svectors[0].dimensions(), svectors[0])

    powers = [1] * len(gaussians)

    for _ in range(iterations):
        gaussians, powers = __single_iteration(svectors, gaussians, powers, em_reserve=em_reserve)

    return gaussians


def __validate_vectors(svectors):
    if len(svectors) == 0:
        raise NoSuperVectorsException
    if len(svectors) == 1:
        raise NotEnoughSuperVectorsException
    count_dimensions = svectors[0].dimensions()
    for svec in iter(svectors):
        if svec.dimensions() != count_dimensions:
            raise DifferentNumberOfDimensionsException


def __generate_random_gaussians(n_gaussians, n_dimensions, one_vector):
    gaussians = []
    for _ in range(n_gaussians):
        gaussians.append(Gaussian.generate_random_gaussian(n_dimensions, one_vector))
    return gaussians


def __single_iteration(svectors, gaussians, powers, em_reserve=0):
    """
    Weights is a two dimensional list.
    weights[i] gives the power of each supervector from i-gaussian
    weights[i][j] gives the power of j-supervector from i-gaussian
    """
    all_weights, new_powers = estimation_step(svectors, gaussians, powers, em_reserve=em_reserve)
    new_gaussians = []
    for weights_from_single_gaussian in iter(all_weights):
        new_gaussians.append(maximization_step(svectors, weights_from_single_gaussian))
    return new_gaussians, new_powers


def estimation_step(svectors, gaussians, powers, em_reserve=0):
    probabilities = __calculate_probabilities_by_gaussians(svectors, gaussians, powers, em_reserve=em_reserve)
    # Should powers be calculated before or after probabilities?
    
    weights = __probabilities_to_weights(probabilities)
    new_powers = __get_gaussian_powers_from_weights(weights)
    return weights, new_powers


def __get_gaussian_powers_from_weights(probabilities):
    powers = []
    for p in iter(probabilities):
        powers.append(sum(p) / len(p))
    return powers


def __calculate_probabilities_by_gaussians(svectors, gaussians, powers, em_reserve=0):
    probabilities = []
    for i in range(len(gaussians)):
        probabilities_from_single_gaussian = []
        for svec in iter(svectors):
            probabilities_from_single_gaussian.append(powers[i] * gaussians[i].get_probability_for_position(svec.matrix(), em_reserve=em_reserve))
        probabilities.append(probabilities_from_single_gaussian)
    return probabilities


def __probabilities_to_weights(probabilities):
    weights = []
    sums = np.array([0] * len(probabilities[0]), dtype=float)
    for p in iter(probabilities):
        weights.append(np.array(p, dtype=float))
        sums += weights[len(weights)-1]
    
    for i in range(len(weights)):
        weights[i] /= sums
    
    return weights


def maximization_step(svectors, weights):
    mean = __super_vectors_mean(svectors, weights)
    sigma = __super_vectors_sigma(svectors, mean, weights)
    return Gaussian(mean, sigma)


def __super_vectors_mean(svectors, weights):
    dimensions = svectors[0].dimensions()
    mean = np.array([0] * dimensions, dtype=float)
    for i in range(dimensions):
        for svec_id in range(len(svectors)):
            mean[i] += svectors[svec_id].component(i) * weights[svec_id]
        mean[i] /= sum(weights)
    return mean


def __super_vectors_sigma(svectors, mean, weights):
    dimensions = svectors[0].dimensions()
    values_from_dimensions = __supervectors_to_array_of_values_for_each_dimension(svectors)
    sigma = np.array([0] * dimensions, dtype=float)
    for i in range(dimensions):
        sigma[i] = __weighted_variance(mean[i], values_from_dimensions[i], weights)
        if math.isclose(sigma[i], 0, abs_tol=3.0e-20):
            # print(sigma[i][i])
            raise NoVarianceException
            # sigma[i] = 3.0e-20
    return sigma


def __weighted_variance(mean, values, weights):
    result = 0
    for i in range(len(values)):
        result += ((values[i]-mean)**2) * weights[i]
    result /= sum(weights)
    return result


def __supervectors_to_array_of_values_for_each_dimension(svectors):
    dimensions = svectors[0].dimensions()
    values = []
    for i in range(dimensions):
        values_from_dimension = []
        for j in range(len(svectors)):
            values_from_dimension.append(svectors[j].component(i))
        values.append(values_from_dimension)
    return values