import numpy as np

from scipy.stats import multivariate_normal as mvn

from src.gaussian import Gaussian

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