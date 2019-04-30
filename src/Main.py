import numpy as np
import json

from scipy.stats import multivariate_normal as mvn

from src.gui.ui import Ui
from src.em import EM
import src.tests.test_em
from src.gaussian import Gaussian

x = json.loads('["foo",        \n {"bar":["baz", null, 1.0, 2]}]')

print(x)
print(x[1]["bar"])


x[1]["pupa"] = ["ala", "mma", "arachnofobie"]

print(x[1])

abc = ['ala', "ma", {"x": "statyw"}]

cde = json.JSONEncoder().encode(abc)
print(cde)
fgh = json.JSONDecoder().decode(cde)
print(fgh)



# TODO: Move it as a test case for em algorithm
# data = np.array([
#         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0],
#         [0, 0, 0, 0, 0, 1, 2, 3, 2, 1, 0],
#         [0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
#         [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]], np.float)


# meh = EM(3, 3)
# gaussians = meh.estimate_gaussians_from_mfcc_data(data)
# print(gaussians[0].get_top_position())
# print(gaussians[1].get_top_position())
# print(gaussians[2].get_top_position())


# ui = Ui()

# ui.start()