from src.super_vector import SuperVector
import src.em as em
from src.gaussian import Gaussian

class Command:
    def __init__(self, name, gaussians):
        self.name = name
        self.gaussians = gaussians


    @classmethod
    def init_from_mfccphrase(cls, mfccphrase, em_gaussians, em_iterations):
        vectors = []
        for i in range(mfccphrase.count_mfccs()):
            vectors.append(SuperVector.init_from_mfcc(mfccphrase.get_mfcc(i)))
        gaussians = em.estimate_n_gaussians(vectors, em_gaussians, em_iterations)
        return Command(mfccphrase.get_name(), gaussians)


    # TODO: Refactor this
    def get_probability_of_this_command(self, supervector):
        if len(supervector) != len(self.gaussians[0].get_mean()):
            return 0
        result = 0
        for g in iter(self.gaussians):
            result += g.get_probability_for_position(supervector)
        return result


    def to_json_obj(self):
        return {
            Command.__COMMAND_NAME: self.name,
            Command.__GAUSSIANS: self.__gaussians_to_json_obj()
        }

    
    def __gaussians_to_json_obj(self):
        obj = []
        for g in iter(self.gaussians):
            obj.append(g.to_json_object())
        return obj

    
    @classmethod
    def from_json_obj(cls, obj):
        return Command(
            obj[Command.__COMMAND_NAME],
            cls.__gaussians_from_json(obj[Command.__GAUSSIANS])
        )


    @classmethod
    def __gaussians_from_json(cls, obj):
        gaussians = []
        for g in iter(obj):
            gaussians.append(Gaussian.from_json_obj(g))
        return obj


    __COMMAND_NAME = "name"
    __GAUSSIANS = "gaussians"
