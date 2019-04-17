from src.mfcc import MFCCParser
import statistics


class EM:
    """
    Class EM represents EM algorithm designed for extracting
    gauss distributions for set of MFCC data.\n
    Parameters:\n
    
    phonem_length - length of single phonem class represented as
    number of MFCC vectors that will be used to describe it.\n
    
    gaussian_models - number of gauss distributions that will be
    resolved from single phonem MFCC data to be representantive
    for this phonem class.
    """

    def __init__(self, phonem_length, gaussian_models):
        self.__phonem_length = phonem_length
        self.__gaussian_models = gaussian_models

    def estimate_gaussians_from_mfcc_data(self, mfcc_data):
        """
        Uses EM algorithm to estimate gaussian distributions for
        passed mfcc data.
        """
        data = MFCCParser.enlarge_each_cell_to_be_positive(mfcc_data)
        # statistics.pvariance()

    # def 

