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
            if gaussian.is_equal_to(expected_gaussians[i], tolerance=0.1) and i not in expected_ids_matched:
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

        cov = np.array([3, 2], dtype=float)
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
            SuperVector([3, 5, 5, 3])
        ]

        gaussians = em.estimate_n_gaussians(svectors, 1, 1)
        self.assertEqual(len(gaussians), 1, "Invalid number of estimated gaussians!")

        gaussians = em.estimate_n_gaussians(svectors, 3, 1)
        self.assertEqual(len(gaussians), 3, "Invalid number of estimated gaussians!")

        gaussians = em.estimate_n_gaussians(svectors, 18, 1)
        self.assertEqual(len(gaussians), 18, "Invalid number of estimated gaussians!")


    def test_estimating_one_gaussian(self):
        svectors = [
            SuperVector([1, 3, 2]),
            SuperVector([3, 5, 1])
        ]
        gaussians = em.estimate_n_gaussians(svectors, 1, 1)

        expected_mean = np.array([2, 4, 1.5], dtype=float)
        expected_cov = np.array([1, 1, 0.25], dtype=float)

        expected_gaussians = [Gaussian(expected_mean, expected_cov)]

        self.assertTrue(are_gaussians_equal(gaussians, expected_gaussians))


    def test_estimating_two_2d_gaussians(self):
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
        gaussians = em.estimate_n_gaussians(svectors, 2, 40)

        expected_first_mean = np.array([1, 1], dtype=float)
        expected_second_mean = np.array([5, 5], dtype=float)

        expected_first_cov = np.array([1, 1], dtype=float)
        expected_second_cov = np.array([0.4, 0.4], dtype=float)

        expected_gaussians = [Gaussian(expected_first_mean, expected_first_cov), 
            Gaussian(expected_second_mean, expected_second_cov)]

        self.assertTrue(are_gaussians_equal(gaussians, expected_gaussians))


    def test_estimating_two_3d_gaussians(self):
        svectors = [
            SuperVector([0, 0, 0]),
            SuperVector([0, 2, 0]),
            SuperVector([2, 0, 0]),
            SuperVector([2, 2, 0]),
            SuperVector([0, 0, 2]),
            SuperVector([0, 2, 2]),
            SuperVector([2, 0, 2]),
            SuperVector([2, 2, 2]),

            SuperVector([5, 5, 5]),
            SuperVector([5, 4, 5]),
            SuperVector([5, 6, 5]),
            SuperVector([4, 5, 5]),
            SuperVector([6, 5, 5]),
            SuperVector([5, 5, 4]),
            SuperVector([5, 5, 6]),
        ]
        gaussians = em.estimate_n_gaussians(svectors, 2, 7)

        expected_first_mean = np.array([1, 1, 1], dtype=float)
        expected_second_mean = np.array([5, 5, 5], dtype=float)

        expected_first_cov = np.array([1, 1, 1], dtype=float)
        expected_second_cov = np.array([0.285714, 0.285714, 0.285714], dtype=float)

        expected_gaussians = [Gaussian(expected_first_mean, expected_first_cov), 
            Gaussian(expected_second_mean, expected_second_cov)]

        self.assertTrue(are_gaussians_equal(gaussians, expected_gaussians))


    def test_estimating_three_2d_gaussians(self):
        svectors = [
            SuperVector([0, 0]),
            SuperVector([0, 2]),
            SuperVector([2, 0]),
            SuperVector([2, 2]),
            SuperVector([7, 9]),
            SuperVector([9, 7]),
            SuperVector([7, 7]),
            SuperVector([9, 9]),
            SuperVector([5, 5]),
            SuperVector([5, 4]),
            SuperVector([5, 6]),
            SuperVector([4, 5]),
            SuperVector([6, 5]),
        ]
        gaussians = em.estimate_n_gaussians(svectors, 3, 13)

        expected_first_mean = np.array([1, 1], dtype=float)
        expected_second_mean = np.array([8, 8], dtype=float)
        expected_third_mean = np.array([5, 5], dtype=float)

        expected_first_cov = np.array([1, 1], dtype=float)
        expected_second_cov = np.array([1, 1], dtype=float)
        expected_third_cov = np.array([0.4, 0.4], dtype=float)

        expected_gaussians = [Gaussian(expected_first_mean, expected_first_cov), 
            Gaussian(expected_second_mean, expected_second_cov),
            Gaussian(expected_third_mean, expected_third_cov)]

        print("expected")
        print(expected_gaussians[0].get_mean())
        print(expected_gaussians[0].get_covariance())

        print("actual")
        print(gaussians[0].get_mean())
        print(gaussians[0].get_covariance())

        self.assertTrue(are_gaussians_equal(gaussians, expected_gaussians))


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