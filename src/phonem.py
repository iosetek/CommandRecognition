

class Phonem:
    """
    Phonem object represents a small part of command.
    Each of them is represented by set of gaussian
    models.
    """

    def __init__(self, em_algorithm, mfcc_data):
        self.__gaussians = em_algorithm.estimate_gaussians_from_mfcc_data(mfcc_data)

    def compare(self, phonem):
        print("TODO")