from src.gui.ui import Ui
from src.em import EM
import numpy as np
# import src.tests.test_enlarge_each_cell
from src.gaussian import Gaussian
from statsmodels.stats.weightstats import DescrStatsW
from scipy.stats import multivariate_normal as mvn


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

g1 = Gaussian(3, 4, 1, 2)
g2 = Gaussian(1, 0, 3, 3)

xs = np.array([
        [-1, 1],
        [1, -1],
        [0.5, 1],
        [1, 0.5],
        [1, 1],
        [2, 1],
        [1, 2],
        [1, 5],
        [2, 4],
        [3, 5],
        [3, 4],
        [3, 3],
        [4, 1],
        [5, 4],
        [5, 2],
        [6, 1]], np.float)

pis = [0.4, 0.6]
mus = [[3, 4], [1, 0]]
sigmas = [[[1, 0], [0, 2]], [[3, 0], [0, 3]]]

# mus = np.array([[3, 4], [[1, 0]]])
# sigmas = np.array([[[3, 0], [0, 0.5]], [[1,0],[0,2]]])
# pis = np.array([0.4, 0.6])

n, p = xs.shape
k = len(pis)

exp_A = []
exp_B = []
ll_new = 0

# E-step
ws = np.zeros((k, n))
for j in range(len(mus)):
    for i in range(n):
        print(mvn(mus[j], sigmas[j]).pdf(xs[i]))
        ws[j, i] = pis[j] * mvn(mus[j], sigmas[j]).pdf(xs[i])
print("ws")
print(ws)
ws /= ws.sum(0)

print("ws")
print(ws)

# M-step
pis = np.zeros(k)
for j in range(len(mus)):
    for i in range(n):
        pis[j] += ws[j, i]
print("pis")
print(pis)

pis /= n

print("pis")
print(pis)

mus = np.zeros((k, p))
for j in range(k):
    for i in range(n):
        mus[j] += ws[j, i] * xs[i]
    mus[j] /= ws[j, :].sum()

print("mus")
print(mus)

sigmas = np.zeros((k, p, p))
for j in range(k):
    for i in range(n):
        ys = np.reshape(xs[i]- mus[j], (2,1))
        sigmas[j] += ws[j, i] * np.dot(ys, ys.T)
    sigmas[j] /= ws[j,:].sum()

print("sigmas")
print(sigmas)

# divv = np.array([0.5, 1], np.float)

# print("sum")
# print(ws.sum(0))

# print("kek")
# print(ws / divv)

# _mus = np.array([[0,4], [2,0]])
# _sigmas = np.array([[[3, 0], [0, 0.5]], [[1,0],[0,2]]])
# _pis = np.array([0.6, 0.4])

# ll_new, pis, mus, sigmas = em_gmm_orig(data, _pis, _mus, _sigmas)

# np.random.seed(123)

# create data set
# n = 10
# _mus = np.array([[0,4], [-2,0]])
# _sigmas = np.array([[[3, 0], [0, 0.5]], [[1,0],[0,2]]])
# _pis = np.array([0.6, 0.4])
# xs = np.concatenate([np.random.multivariate_normal(mu, sigma, int(pi*n))
#                     for pi, mu, sigma in zip(_pis, _mus, _sigmas)])

# print(xs)

# weighted_stats = DescrStatsW([0, 1], weights=[1, 1.5], ddof=0)
# # print(weighted_stats.var)
# print(weighted_stats.mean)

# meh = EM(3, 3)
# gaussians = meh.estimate_gaussians_from_mfcc_data(data)
# print(gaussians[0].get_top_position())
# print(gaussians[1].get_top_position())
# print(gaussians[2].get_top_position())

# temp1 = Gaussian(3, 1, 0.31, 0.34)
# temp2 = Gaussian(7, 5, 0.93, 1)


# ui = Ui()

# ui.start()