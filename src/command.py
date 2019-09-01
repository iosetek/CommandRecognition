from src.super_vector import SuperVector
import src.em as em

class Command:
    def __init__(self, name, gaussians):
        self.name = name
        self.gaussians = gaussians


    @classmethod
    def init_from_mfccphrase(cls, mfccphrase, em_gaussians, em_iterations, em_reserve=0):
        vectors = []
        for i in range(mfccphrase.count_mfccs()):
            vectors.append(SuperVector.init_from_mfcc(mfccphrase.get_mfcc(i)))
        gaussians = em.estimate_n_gaussians(vectors, em_gaussians, em_iterations, em_reserve=em_reserve)
        return Command(mfccphrase.get_name(), gaussians)


    # TODO: Refactor this
    def get_probability_of_this_command(self, supervector, em_reserve=0):
        if len(supervector) != len(self.gaussians[0].get_mean()):
            return 0
        result = 0
        for g in iter(self.gaussians):
            result += g.get_probability_for_position(supervector, em_reserve=em_reserve)
        return result