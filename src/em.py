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

def estimate_n_gaussians(svectors, n_gaussians, iterations):
    __validate_vectors(svectors)

    gaussians = __generate_random_gaussians(n_gaussians, svectors[0].dimensions())

    for _ in range(iterations):
        gaussians = __single_iteration(svectors, gaussians)

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


def __generate_random_gaussians(n_gaussians, n_dimensions):
    gaussians = []
    for _ in range(n_gaussians):
        gaussians.append(Gaussian.generate_random_gaussian(n_dimensions))
    return gaussians


def __single_iteration(svectors, gaussians):
    all_weigths = estimation_step(svectors, gaussians)
    new_gaussians = []
    for weights_from_single_gaussian in iter(all_weigths):
        new_gaussians.append(maximization_step(svectors, weights_from_single_gaussian))
    return new_gaussians


def estimation_step(svectors, gaussians):
    probabilities = __calculate_probabilities_by_gaussians(svectors, gaussians)
    return __probabilities_to_weights(probabilities)


def __calculate_probabilities_by_gaussians(svectors, gaussians):
    probabilities = []
    for gaussian in iter(gaussians):
        probabilities_from_single_gaussian = []
        for svec in iter(svectors):
            probabilities_from_single_gaussian.append(gaussian.get_probability_for_position(svec.matrix()))
        probabilities.append(probabilities_from_single_gaussian)
    return probabilities


def __probabilities_to_weights(probabilities):
    sums = []
    count_gaussians = len(probabilities)
    count_svectors = len(probabilities[0])
    for vector_id in range(count_svectors):
        sums.append(__sum_probabilities(probabilities, vector_id))
    
    for vector_id in range(count_svectors):
        for gaussian_id in range(count_gaussians):
            probabilities[gaussian_id][vector_id] /= sums[vector_id]

    return probabilities
    


def __sum_probabilities(probabilities, svec_id):
    sum = 0
    for gaussian_id in range(len(probabilities)):
        sum += probabilities[gaussian_id][svec_id]
    return sum


def maximization_step(svectors, weights):
    mean = __super_vectors_mean(svectors, weights)
    sigma = __super_vectors_sigma(svectors, mean, weights)
    return Gaussian(mean, sigma)


def __calculate_weigths(svectors, gaussians):
    weigths = [0] * len(svectors)
    # TODO


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
    sigma = np.array([[0] * dimensions] * dimensions, dtype=float)
    for i in range(dimensions):
        for j in range(dimensions):
            if i == j:
                sigma[i][i] = np.var(values_from_dimensions[i], dtype=float)
                if math.isclose(sigma[i][i], 0, abs_tol=0.00001):
                    raise NoVarianceException
            else:
                cov = np.cov(values_from_dimensions[i], values_from_dimensions[j])
                # TODO: Calculate only one field from that covariance matrix
                covs = cov[0][1]
                sigma[i][j] = covs
                sigma[j][i] = covs
    return sigma


def __supervectors_to_array_of_values_for_each_dimension(svectors):
    dimensions = svectors[0].dimensions()
    values = []
    for i in range(dimensions):
        values_from_dimension = []
        for j in range(len(svectors)):
            values_from_dimension.append(svectors[j].component(i))
        values.append(values_from_dimension)
    return values