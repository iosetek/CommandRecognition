import math
import numpy as np
import random
import statistics
from src.gaussian import Gaussian
from src.super_vector import SuperVector

supervectors_with_diff_dimensions_exception = "Super Vectors with different number of dimensions"
not_enough_supervectors_exception = "Not enough Super Vectors"
null_variance_exception = "Null Variance"


def estimate_n_gaussians(svectors, n_gaussians, iterations):
    __validate_vectors(svectors)

    gaussians = __generate_random_gaussians(n_gaussians)

    for i in range(iterations):
        gaussians = __single_iteration(svectors, gaussians)

    return gaussians


def __validate_vectors(svectors):
    if len(svectors) == 0:
        raise Exception("Cannot use EM algorithm without any super vector")
    count_dimensions = svectors[0].dimensions()
    for svec in iter(svectors):
        if svec.dimensions() != count_dimensions:
            raise Exception("Got super vector with different amount of dimensions than others")


def __generate_random_gaussians(n_gaussians, n_dimensions):
    gaussians = []
    for i in range(n_gaussians):
        gaussians.append(Gaussian.generate_random_gaussian(n_dimensions))
    return gaussians


def __single_iteration(svectors, gaussians):
    all_weigths = estimation_step(svectors, gaussians)
    new_gaussians = []
    for weights_from_single_gaussian in iter(all_weigths):
        new_gaussians.append(maximization_step(svectors, weights_from_single_gaussian))
    return weigths


def estimation_step(svectors, gaussians):
    probabilities = __calculate_probabilities_by_gaussians(svectors, gaussians)
    return __probabilities_to_weights(probabilities)


def __calculate_probabilities_by_gaussians(svectors, gaussians):
    probabilities = []
    for gaussian in iter(gaussians):
        probabilities_from_single_gaussian = []
        for svec in iter(svectors):
            probabilities_from_single_gaussian.append(gaussian.get_probability_for_position(svec))
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



def __calculate_weigths(svectors, gaussians):
    weigths = [0] * len(svectors)
    # TODO


def __super_vectors_mean(svectors, weights):
    dimensions = svectors[0].dimensions()
    mean = [0] * dimensions
    for i in range(dimensions):
        for svec_id in range(len(svectors)):
            mean[i] += svectors[svec_id][i] * weights[svec_id]
        mean[i] /= sum(weights)
    return mean


def __super_vectors_sigma(svectors, mean, weights):
    dimensions = svectors[0].dimensions()
    values_from_dimensions = __supervectors_to_array_of_values_for_each_dimension(svectors)
    sigma = [[0] * dimensions] * dimensions
    for i in range(dimensions):
        for j in range(dimensions):
            if i == j:
                sigma[i][i] = np.var(values_from_dimensions[i], dtype=float)
            else:
                cov = np.cov(values_from_dimensions[i], values_from_dimensions[j])
                sigma[i][j] = cov
                sigma[j][i] = cov
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