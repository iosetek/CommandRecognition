import unittest
import numpy as np
import os
import math
from src.super_vector import SuperVector
from src.mfcc import MFCC
import src.em as em

class TestEnlargeEachCell(unittest.TestCase):
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
        with self.assertRaises(Exception) as exc:
            em.estimate_n_gaussians([], 1, 20)
        self.assertTrue(em.not_enough_supervectors_exception in exc.exception)


    def test_estimating_from_supervectors_with_different_amount_of_dimensions(self):
        svectors = [
            SuperVector([0, 0]),
            SuperVector([0, 2, 4])
        ]
        with self.assertRaises(Exception) as exc:
            em.estimate_n_gaussians(svectors, 1, 20)
        self.assertTrue(em.supervectors_with_diff_dimensions_exception in exc.exception)


    def test_estimate_gaussian_from_supervectors_with_same_one_dimension(self):
        svectors = [
            SuperVector([4, 0, 3]),
            SuperVector([4, 2, 4]),
            SuperVector([4, 3, 4]),
            SuperVector([4, 1, 2]),
            SuperVector([4, 5, 1]),
        ]
        with self.assertRaises(Exception) as exc:
            em.estimate_n_gaussians(svectors, 1, 20)
        self.assertTrue(em.null_variance_exception in exc.exception)


    def test_estimate_gaussian_from_supervectors_with_no_variance_at_all(self):
        svectors = [
            SuperVector([4, 4, 4]),
            SuperVector([4, 4, 4]),
            SuperVector([4, 4, 4]),
        ]
        with self.assertRaises(Exception) as exc:
            em.estimate_n_gaussians(svectors, 1, 20)
        self.assertTrue(em.null_variance_exception in exc.exception)


    def test_estimate_gaussian_from_single_supervector(self):
        svectors = [SuperVector([0, 0])]
        with self.assertRaises(Exception) as exc:
            em.estimate_n_gaussians(svectors, 1, 20)
        self.assertTrue(em.not_enough_supervectors_exception in exc.exception)