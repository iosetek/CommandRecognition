import json
import numpy as np

from src.mfcc import MFCC
from src.plot_drawer import PlotDrawer

class MfccCommand:
    """
    Single command representation using MFCC data.
    """
    def __init__(self, name, data):
        self.__name = name
        self.__data = data


    @classmethod
    def from_json_file(cls, json_filename):
        file = open(json_filename, "r")
        json_str = file.read()
        file.close()
        # TODO Handle that
        json_str = json.JSONDecoder().decode(json_str)
        name = json_str["name"]
        data = MFCC(np.array(json_str["data"], dtype=float))
        return cls(name, data)


    def save_to_json_file(self, json_filename):
        file = open(json_filename, "w")
        obj_as_dict = dict()
        obj_as_dict["name"] = self.__name
        obj_as_dict["data"] = self.__data.get_data().tolist()
        json_str = json.JSONEncoder().encode(obj_as_dict)
        file.write(json_str)
        file.close()


    def get_data(self):
        return self.__data


    def normalize_to(self, value):
        return self.__data.normalize_to(value)

    
    def get_name(self):
        return self.__name


    def multiply_data(self, by):
        self.__data.multiply_values(by)


    def enlarge_each_cell_to_be_positive(self):
        self.__data.enlarge_each_cell_to_be_positive()


    def draw_mfcc(self):
       PlotDrawer.draw(self.__data.get_data()) 

    #TODO Delete this
    def erase_some_mfcc(self):
        self.__data.erase_some_mfcc()
