import json
import numpy as np

from src.mfcc import MFCC

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

    
    def get_name(self):
        return self.__name
