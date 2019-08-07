import json
import numpy as np
import math

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
    

    def get_diff_with_other_command_measuring_top_height(self, gauss_comm):
        if len(self.__gaussians) != len(gauss_comm.get_gaussians()):
            print("UNHANDLED SITUATION. TWO COMMANDS SHOULD HAVE EQUAL NUMBER OF GAUSSIANS")
            return
        self.ensure_gaussians_are_sorted()
        gauss_comm.ensure_gaussians_are_sorted()
        difference = 0

        for i in range(len(self.__gaussians)):
            difference += math.fabs(self.__gaussians[i].get_top_position()[1] - 
                        gauss_comm.get_gaussians()[i].get_top_position()[1]) ** 3

        return difference


    def get_diff_with_other_command_measuring_top_height_and_differences_multiplied(self, gauss_comm):
        if len(self.__gaussians) != len(gauss_comm.get_gaussians()):
            print("UNHANDLED SITUATION. TWO COMMANDS SHOULD HAVE EQUAL NUMBER OF GAUSSIANS")
            return
        self.ensure_gaussians_are_sorted()
        gauss_comm.ensure_gaussians_are_sorted()
        diffPosition = 0

        for i in range(len(self.__gaussians)):
            diffPosition += math.fabs(self.__gaussians[i].get_top_position()[1] - 
                        gauss_comm.get_gaussians()[i].get_top_position()[1]) ** 2

        other_diff = 0
        for i in range(1, len(self.__gaussians)):
            orig_diff = self.__gaussians[i].get_top_position()[1] - self.__gaussians[i-1].get_top_position()[1]
            oth_diff = gauss_comm.get_gaussians()[i].get_top_position()[1] - gauss_comm.get_gaussians()[i-1].get_top_position()[1]
            other_diff += math.fabs(orig_diff - oth_diff) ** 4
        return diffPosition * other_diff


    def get_diff_with_other_command_measuring_top_height_and_differences_summed_up(self, gauss_comm):
        if len(self.__gaussians) != len(gauss_comm.get_gaussians()):
            print("UNHANDLED SITUATION. TWO COMMANDS SHOULD HAVE EQUAL NUMBER OF GAUSSIANS")
            return
        self.ensure_gaussians_are_sorted()
        gauss_comm.ensure_gaussians_are_sorted()
        diffPosition = 0

        for i in range(len(self.__gaussians)):
            diffPosition += math.fabs(self.__gaussians[i].get_top_position()[1] - 
                        gauss_comm.get_gaussians()[i].get_top_position()[1]) ** 2

        other_diff = 0
        for i in range(1, len(self.__gaussians)):
            orig_diff = self.__gaussians[i].get_top_position()[1] - self.__gaussians[i-1].get_top_position()[1]
            oth_diff = gauss_comm.get_gaussians()[i].get_top_position()[1] - gauss_comm.get_gaussians()[i-1].get_top_position()[1]
            other_diff += math.fabs(orig_diff - oth_diff) ** 0.5
        return diffPosition + other_diff


    def get_diff_with_other_command(self, gauss_comm):
        if len(self.__gaussians) != len(gauss_comm.get_gaussians()):
            print("UNHANDLED SITUATION. TWO COMMANDS SHOULD HAVE EQUAL NUMBER OF GAUSSIANS")
            return
        self.ensure_gaussians_are_sorted()
        gauss_comm.ensure_gaussians_are_sorted()
        diffPosition = 0

        for i in range(len(self.__gaussians)):
            diffPosition += math.fabs(self.__gaussians[i].get_top_position()[1] - 
                        gauss_comm.get_gaussians()[i].get_top_position()[1]) ** 2
            # diffVariance = math.fabs(self.__gaussians[i].get_variances()[1][1] - 
            #             gauss_comm.get_gaussians()[i].get_variances()[1][1]) ** 2 
            # difference += diffPosition * diffVariance

        other_diff = 0
        for i in range(1, len(self.__gaussians)):
            orig_diff = self.__gaussians[i].get_top_position()[1] - self.__gaussians[i-1].get_top_position()[1]
            oth_diff = gauss_comm.get_gaussians()[i].get_top_position()[1] - gauss_comm.get_gaussians()[i-1].get_top_position()[1]
            other_diff += math.fabs(orig_diff - oth_diff) ** 4
        return diffPosition * other_diff
        

    def ensure_gaussians_are_sorted(self):
        gaussians_swapped = True
        while gaussians_swapped:
            gaussians_swapped = False
            for i in range(1, len(self.__gaussians)):
                if self.__gaussians[i].get_top_position()[0] < self.__gaussians[i-1].get_top_position()[0]:
                    temp = self.__gaussians[i]
                    self.__gaussians[i] = self.__gaussians[i-1]
                    self.__gaussians[i-1] = temp
                    gaussians_swapped = True