import unittest
import numpy as np
import os
import math
from src.super_vector import SuperVector
from src.mfcc import MFCC
import src.em as em
from src.gaussian import Gaussian

def are_gaussians_equal(actual_gaussians, expected_gaussians):
    if len(actual_gaussians) != len(expected_gaussians):
        return False
    expected_ids_matched = dict()

    for gaussian in iter(actual_gaussians):
        for i in range(len(expected_gaussians)):
            if gaussian.is_equal_to(expected_gaussians[i]) and i not in expected_ids_matched:
                expected_ids_matched[i] = True
                break
        else:
            return False
    return True


class TestEM(unittest.TestCase):
    def test_are_gaussians_equal_helper_method(self):
        first_list = []
        second_list = []
        self.assertTrue(are_gaussians_equal(first_list, second_list))

        cov = np.array([[3, 0], [0, 2]], dtype=float)
        gaussian_A = Gaussian(np.array([3, 5], dtype=float), cov)
        gaussian_B = Gaussian(np.array([5, 3], dtype=float), cov)
        gaussian_C = Gaussian(np.array([4, 4], dtype=float), cov)

        first_list = [gaussian_A, gaussian_B, gaussian_C]
        second_list = [gaussian_A, gaussian_B, gaussian_C]
        self.assertTrue(are_gaussians_equal(first_list, second_list))
        
        first_list = [gaussian_A, gaussian_B, gaussian_C]
        second_list = [gaussian_C, gaussian_B, gaussian_A]
        self.assertTrue(are_gaussians_equal(first_list, second_list))

        first_list = [gaussian_A, gaussian_B, gaussian_C]
        second_list = [gaussian_C, gaussian_A, gaussian_B]
        self.assertTrue(are_gaussians_equal(first_list, second_list))

        first_list = [gaussian_A, gaussian_B, gaussian_C]
        second_list = [gaussian_C, gaussian_A]
        self.assertFalse(are_gaussians_equal(first_list, second_list))

        first_list = [gaussian_A, gaussian_B, gaussian_C]
        second_list = [gaussian_A, gaussian_B, gaussian_B, gaussian_C]
        self.assertFalse(are_gaussians_equal(first_list, second_list))

        first_list = [gaussian_A, gaussian_B, gaussian_C]
        second_list = [gaussian_A, gaussian_B, gaussian_B, gaussian_C]
        self.assertFalse(are_gaussians_equal(first_list, second_list))

        first_list = [gaussian_A, gaussian_B, gaussian_C]
        second_list = [gaussian_A, gaussian_B, gaussian_B]
        self.assertFalse(are_gaussians_equal(first_list, second_list))

        gaussian_D = Gaussian(np.array([4, 4], dtype=float), cov)
        first_list = [gaussian_A, gaussian_B, gaussian_C]
        second_list = [gaussian_D, gaussian_B, gaussian_A]
        self.assertTrue(are_gaussians_equal(first_list, second_list))


    def test_correct_number_of_estimated_gaussians(self):
        svectors = [
            SuperVector([1, 3, 2, 4]),
            SuperVector([3, 5, 2, 3])
        ]

        gaussians = em.estimate_n_gaussians(svectors, 1, 1)
        self.assertEqual(len(gaussians), 1, "Invalid number of estimated gaussians!")

        gaussians = em.estimate_n_gaussians(svectors, 3, 1)
        self.assertEqual(len(gaussians), 3, "Invalid number of estimated gaussians!")

        gaussians = em.estimate_n_gaussians(svectors, 18, 1)
        self.assertEqual(len(gaussians), 7, "Invalid number of estimated gaussians!")


    def test_estimating_one_gaussian(self):
        svectors = [
            SuperVector([1, 3, 2]),
            SuperVector([3, 5, 1])
        ]
        gaussians = em.estimate_n_gaussians(svectors, 1, 1)

        expected_mean = [2, 4, 1.5]
        expected_cov = [
            [1,     1,      -0.5],
            [1,     1,      -0.5],
            [-0.5,  -0.5,   0.25]
        ]

        self.assertEqual(gaussians[0].get_mean(), expected_mean, "Mean calculated incorrectly!")
        self.assertEqual(gaussians[0].get_covariance(), expected_cov, "Covariance calculated incorrectly!")


    def test_estimating_two_gaussians(self):
        svectors = [
            SuperVector([0, 0]),
            SuperVector([0, 2]),
            SuperVector([2, 0]),
            SuperVector([2, 2]),
            SuperVector([5, 5]),
            SuperVector([5, 4]),
            SuperVector([5, 6]),
            SuperVector([4, 5]),
            SuperVector([6, 5]),
        ]
        gaussians = em.estimate_n_gaussians(svectors, 1, 20)

        expected_first_mean = [1, 1]
        expected_second_mean = [5, 5]

        expected_first_cov = [[1, 0], [0, 1]]
        expected_second_cov = [[0.4, 0], [0, 0.4]]

        if gaussians[0].get_mean()[0] > gaussians[1].get_mean()[0]:
            gaussians.reverse()

        self.assertEqual(gaussians[0].get_mean(), expected_first_mean, "Mean calculated incorrectly!")
        self.assertEqual(gaussians[0].get_covariance(), expected_first_cov, "Covariance calculated incorrectly!")

        self.assertEqual(gaussians[1].get_mean(), expected_second_mean, "Mean calculated incorrectly!")
        self.assertEqual(gaussians[1].get_covariance(), expected_second_cov, "Covariance calculated incorrectly!")


    def test_estimating_from_empty_supervectors(self):
        with self.assertRaises(em.NoSuperVectorsException):
            em.estimate_n_gaussians([], 1, 20)


    def test_estimating_from_supervectors_with_different_amount_of_dimensions(self):
        svectors = [
            SuperVector([0, 0]),
            SuperVector([0, 2, 4])
        ]
        with self.assertRaises(em.DifferentNumberOfDimensionsException):
            em.estimate_n_gaussians(svectors, 1, 20)


    def test_estimate_gaussian_from_supervectors_with_same_one_dimension(self):
        svectors = [
            SuperVector([4, 0, 3]),
            SuperVector([4, 2, 4]),
            SuperVector([4, 3, 4]),
            SuperVector([4, 1, 2]),
            SuperVector([4, 5, 1]),
        ]
        with self.assertRaises(em.NoVarianceException):
            em.estimate_n_gaussians(svectors, 1, 20)


    def test_estimate_gaussian_from_supervectors_with_no_variance_at_all(self):
        svectors = [
            SuperVector([4, 4, 4]),
            SuperVector([4, 4, 4]),
            SuperVector([4, 4, 4]),
        ]
        with self.assertRaises(em.NoVarianceException):
            em.estimate_n_gaussians(svectors, 1, 20)


    def test_estimate_gaussian_from_single_supervector(self):
        svectors = [SuperVector([0, 0])]
        with self.assertRaises(em.NotEnoughSuperVectorsException):
            em.estimate_n_gaussians(svectors, 1, 20)