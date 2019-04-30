# Based on http://people.duke.edu/~ccc14/sta-663/EMAlgorithm.html
from scipy.stats import multivariate_normal as mvn
import numpy as np
import math
import unittest
from src.gaussian import Gaussian
from src.em import EM

def single_em(data_positions, pis, mus, sigmas):
    for _ in range(1):
        estimations = e_step(data_positions, pis, mus, sigmas)
        pis, mus, sigmas = m_step(data_positions, estimations)
        gaussians = []
        for i in range(len(pis)):
            gaussians.append(Gaussian(pis[i], mus[i], sigmas[i]))
    return gaussians

def e_step(data_positions, pis, mus, sigmas):
    number_of_gaussians = len(pis)

    number_of_probes, number_of_dimensions = data_positions.shape 

    ws = np.zeros((number_of_gaussians, number_of_probes))
    for gaussian_id in range(number_of_gaussians):
        for probe_id in range(number_of_probes):
            pi = pis[gaussian_id]
            mu = mus[gaussian_id]
            sigma = sigmas[gaussian_id]
            value = pi * mvn(mu, sigma).pdf(data_positions[probe_id])
            ws[gaussian_id, probe_id] = pi * mvn(mu, sigma).pdf(data_positions[probe_id])
    ws /= ws.sum(0)

    return ws

def m_step(data_positions, estimations):
    number_of_dimensions = len(data_positions[0])
    number_of_gaussians = len(estimations)
    
    pis = np.zeros(number_of_gaussians)
    mus = np.zeros((number_of_gaussians, number_of_dimensions))
    sigmas = sigmas = np.zeros((number_of_gaussians, number_of_dimensions, number_of_dimensions))

    for gaussian_id in range(number_of_gaussians):
        pis[gaussian_id] += get_pi_from_estimations(estimations[gaussian_id])

    for gaussian_id in range(number_of_gaussians):
        mus[gaussian_id] += get_mean_from_data_and_estimations(
            data_positions, estimations[gaussian_id])

    for gaussian_id in range(number_of_gaussians):
        sigmas[gaussian_id] += get_sigma_from_data_and_estimations(
            data_positions, estimations[gaussian_id], mus[gaussian_id])

    return pis, mus, sigmas

def get_pi_from_estimations(estimations):
    number_of_probes = len(estimations)
    return (sum(estimations) / number_of_probes)


def get_mean_from_data_and_estimations(data, estimations):
    number_of_probes = len(data)
    number_of_dimensions = len(data[0])
    mean = np.zeros((number_of_dimensions))

    # TODO Check if it cannot be done by multiplification of two vectors
    for i in range(number_of_probes):
        mean += estimations[i] * data[i]

    return (mean / sum(estimations))


def get_sigma_from_data_and_estimations(data, estimations, gaussian_mean):
    number_of_probes = len(data)
    number_of_dimensions = len(data[0])
    sigma = np.zeros((number_of_dimensions, number_of_dimensions))

    for i in range(number_of_probes):
        ys = np.reshape(data[i] - gaussian_mean, (2,1))
        sigma += estimations[i] * np.dot(ys, ys.T)

    return (sigma / sum(estimations))

class TestEM(unittest.TestCase):

    def test_pi_calculation(self):
        # This is in Y X order.
        data = np.array([
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [1, 2, 3, 2, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]])

        probes = np.array([
                [1, 1],
                [1, 2],
                [1, 3],
                [2, 0],
                [2, 1],
                [2, 1],
                [2, 2],
                [2, 2],
                [2, 2],
                [2, 3],
                [2, 3],
                [2, 4],
                [3, 1],
                [3, 2],
                [3, 3]], np.float)

        test_pis = np.array([0.4, 0.6])
        test_mus = np.array([[1, 2], [3.5, 5.5]])
        test_sigmas = np.array([[[3, 0], [0, 1]], [[2, 0], [0, 2]]])

        input_gaussians = [Gaussian(test_pis[0], test_mus[0], test_sigmas[0]), Gaussian(test_pis[1], test_mus[1], test_sigmas[1])]

        expected_gaussians = single_em(probes, test_pis, test_mus, test_sigmas)
        # TODO Set valid parameters
        em_instance = EM(2, 2)
        got_gaussians = em_instance.single_em_iteration(input_gaussians, data)
        
        self.assertTrue(math.isclose(got_gaussians[0].get_pi(), expected_gaussians[0].get_pi(), abs_tol=0.00001))
        self.assertTrue(math.isclose(got_gaussians[1].get_pi(), expected_gaussians[1].get_pi(), abs_tol=0.00001))

        self.assertTrue(math.isclose(got_gaussians[0].get_top_position()[0], expected_gaussians[0].get_top_position()[0], abs_tol=0.00001))
        self.assertTrue(math.isclose(got_gaussians[0].get_top_position()[1], expected_gaussians[0].get_top_position()[1], abs_tol=0.00001))
        self.assertTrue(math.isclose(got_gaussians[1].get_top_position()[0], expected_gaussians[1].get_top_position()[0], abs_tol=0.00001))
        self.assertTrue(math.isclose(got_gaussians[1].get_top_position()[1], expected_gaussians[1].get_top_position()[1], abs_tol=0.00001))

        self.assertTrue(math.isclose(got_gaussians[0].get_variances()[0][0], expected_gaussians[0].get_variances()[0][0], abs_tol=0.00001))
        self.assertTrue(math.isclose(got_gaussians[0].get_variances()[1][0], expected_gaussians[0].get_variances()[1][0], abs_tol=0.00001))
        self.assertTrue(math.isclose(got_gaussians[0].get_variances()[0][1], expected_gaussians[0].get_variances()[0][1], abs_tol=0.00001))
        self.assertTrue(math.isclose(got_gaussians[0].get_variances()[1][1], expected_gaussians[0].get_variances()[1][1], abs_tol=0.00001))
        self.assertTrue(math.isclose(got_gaussians[1].get_variances()[0][0], expected_gaussians[1].get_variances()[0][0], abs_tol=0.00001))
        self.assertTrue(math.isclose(got_gaussians[1].get_variances()[1][0], expected_gaussians[1].get_variances()[1][0], abs_tol=0.00001))
        self.assertTrue(math.isclose(got_gaussians[1].get_variances()[0][1], expected_gaussians[1].get_variances()[0][1], abs_tol=0.00001))
        self.assertTrue(math.isclose(got_gaussians[1].get_variances()[1][1], expected_gaussians[1].get_variances()[1][1], abs_tol=0.00001))
