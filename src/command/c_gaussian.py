import json
import numpy as np

from src.gaussian import Gaussian

class GaussianCommand:
    """
    Single command representation using 2D gaussian distributions.
    """
    def __init__(self, name, gaussians):
        self.__name = name
        self.__gaussians = gaussians


    # TODO Handle proper file opening
    @classmethod
    def from_json_file(cls, json_filename):
        file = open(json_filename, "r")
        json_str = file.read()
        file.close()
        # TODO Handle that
        json_str = json.JSONDecoder().decode(json_str)
        name = json_str["name"]
        gaussians_count = len(json_str["gaussians"])
        gaussians = []
        for i in range(gaussians_count):
            pi = json_str["gaussians"][i]["pi"]
            mean = np.array(json_str["gaussians"][i]["mean"], dtype=float)
            var = np.array(json_str["gaussians"][i]["variances"], dtype=float)
            gaussians.append(Gaussian(pi, mean, var))
        return cls(name, gaussians)


    # TODO Handle proper file opening
    def save_to_json_file(self, json_filename):
        file = open(json_filename, "w")
        obj_as_dict = dict()
        obj_as_dict["name"] = self.__name
        obj_as_dict["gaussians"] = []
        for i in range(len(self.__gaussians)):
            obj_as_dict["gaussians"].append(dict())
            obj_as_dict["gaussians"][i]["pi"] = self.__gaussians[i].get_pi()
            obj_as_dict["gaussians"][i]["mean"] = self.__gaussians[i].get_top_position().tolist()
            obj_as_dict["gaussians"][i]["variances"] = self.__gaussians[i].get_variances().tolist()
        json_str = json.JSONEncoder().encode(obj_as_dict)
        file.write(json_str)
        file.close()


    def get_gaussians(self):
        return self.__gaussians

    
    def get_name(self):
        return self.__name
