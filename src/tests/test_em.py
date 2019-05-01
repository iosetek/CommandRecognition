# Based on http://people.duke.edu/~ccc14/sta-663/EMAlgorithm.html
import numpy as np
import math
import unittest

from scipy.stats import multivariate_normal as mvn

from src.gaussian import Gaussian
import src.em as em
import src.tests.base_em as base_em
from src.mfcc import MFCC

def are_2d_gaussians_equal(a, b):
    if not math.isclose(a.get_pi(), b.get_pi(), abs_tol=0.00001):
        return False
    for i in range(2):
        if not math.isclose(a.get_top_position()[i], b.get_top_position()[i], abs_tol=0.00001):
            return False
    for i in range(2):
        for j in range(2):
            if not math.isclose(a.get_variances()[i][j], b.get_variances()[i][j], abs_tol=0.00001):
                return False
    return True


def is_mean_within_gaussians(mean, gaussians):
    for i in range(len(gaussians)):
        g_mean = gaussians[i].get_top_position()
        if math.isclose(mean[0], g_mean[0], abs_tol=0.00001) and math.isclose(mean[1], g_mean[1], abs_tol=0.00001):
            return True 
    return False

class TestEM(unittest.TestCase):

    def test_similarity_of_two_algorithms(self):
        input_mfcc = np.array([
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [1, 2, 3, 2, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]], np.float)

        input_probes = np.array([
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

        input_pis = np.array([0.4, 0.6])
        input_means = np.array([[1, 2], [3.5, 5.5]])
        input_variances = np.array([[[3, 0], [0, 1]], [[2, 0], [0, 2]]])

        input_gaussians = []
        for i in range(len(input_pis)):
            input_gaussians.append(Gaussian(input_pis[i], input_means[i], input_variances[i]))

        expected_gaussians = base_em.single_em(input_probes, input_pis, input_means, input_variances)
        got_gaussians = em.single_em_iteration(input_gaussians, input_mfcc)

        for i in range(len(input_gaussians)):
            self.assertTrue(are_2d_gaussians_equal(expected_gaussians[i], got_gaussians[i]))


    def test_determinism(self):
        input_mfcc = np.array([
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [1, 2, 3, 2, 1],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0]], np.float)

        m = MFCC(input_mfcc)
        extracted_gaussians = []

        for _ in range(10):
            extracted_gaussians.append(m.extract_gaussians(2))

        for i in range(1, 10):
            self.assertTrue(are_2d_gaussians_equal(extracted_gaussians[0][0], extracted_gaussians[i][0]))
            self.assertTrue(are_2d_gaussians_equal(extracted_gaussians[0][1], extracted_gaussians[i][1]))

    
    def test_algorithm(self):
        data = np.array([
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0],
            [0, 0, 0, 0, 0, 1, 2, 3, 2, 1, 0],
            [0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]], np.float)

        expected_means = []
        expected_means.append(np.array([8.5, 0.5], dtype=float))
        expected_means.append(np.array([1, 3], dtype=float))
        expected_means.append(np.array([5, 7], dtype=float))

        m = MFCC(data)
        gaussians = m.extract_gaussians(3)

        for i in range(len(expected_means)):
            self.assertTrue(is_mean_within_gaussians(expected_means[i], gaussians))
