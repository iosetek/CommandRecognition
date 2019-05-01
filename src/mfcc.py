import numpy as np
import math
import scipy.io.wavfile as wav

from python_speech_features import mfcc as mfcc_extractor

import src.em as em

class MFCC:
    """
    Class designed to hold an array filled up with MFCC data.
    """
    def __init__(self, data):
        self.__data = data
        self.__frames_count = len(data)
        if self.__frames_count == 0:
            self.__coefficients_count = 0
        else:    
            self.__coefficients_count = len(data[0])


    @classmethod
    def from_track(cls, track_filename,
                    window_function = np.hamming, window_length = 0.03, distance_to_next_window = 0.01,
                    cepstral_amount = 13, filters_amount = 30,
                    fft_size = 1024,
                    append_energy = True,
                    low_freq = 0, max_freq = None,
                    preemph_filter = 0.97, cep_lifter = 22):
        """
            Constructs MFCC object from wav file.\n
            Parameters:\n
            track_filename - path and the name of the wav file,
            window_function - function for extracting single window from sound track,\n
                example: numpy.hamming
            window_length - size of single window measured in seconds,\n
            distance_to_next_window - the distance to next window measured in seconds,\n
            cepstral_amount - number of cepstral coefficients that are extracted from track and stored in single window,\n
            filters_amount - number of MEL filters used for extraction,\n
            fft_size - TODO\n
            append_energy - if True the zeroth cepstral coefficient is replaced with the log of the total frame energy,\n
            low_freq - the lowest frequency that will be considered in extraction,\n
            max_freq - the highest frequency that will be considered in extraction,\n
            preemph_filter - the power of preemphasis filter. Min: 0, Max: 1,\n
            cep_lifter - the power of lifter that will be added to final cepstral coefficients.\n
        """
        rate, signal = wav.read(track_filename)
        return cls(mfcc_extractor(
                signal=signal(),
                samplerate=rate(),
                winlen=window_length,
                winstep=distance_to_next_window,
                numcep=cepstral_amount,
                nfilt=filters_amount,
                nfft=fft_size,
                lowfreq=low_freq,
                highfreq=max_freq,
                preemph=preemph_filter,
                ceplifter=cep_lifter,
                appendEnergy=append_energy,
                winfunc=window_function))

    
    def convert_to_n_frames(self, n):
        """
        Converts data to fill more or less frames.
        """
        if len(self.__data) == 0 or len(self.__data) == n:
            return
        if len(self.__data) > n:
            self.__convert_reduction(n)
            return
        self.__convert_elongation(n)


    def __convert_elongation(self, n):
        converted = np.array([[0] * self.__coefficients_count] * n, dtype=float)

        for i in range(n):
            previous_index = math.floor((i*self.__frames_count)/n)
            next_index = previous_index + 1
            
            # TODO: Refactor this!
            # this is a temporary workaround to ignore nextIndex when it's out of bounds.
            if next_index == self.__frames_count:
                next_index -= 1

            previous_value_weight = n - ((i*self.__frames_count)%n)
            if previous_value_weight > self.__frames_count:
                next_value_weight = 0
            else:
                next_value_weight = self.__frames_count - previous_value_weight

            for j in range(self.__coefficients_count):
                previous_value = self.__data[previous_index][j]
                next_value = self.__data[next_index][j]
                converted[i][j] = self.__get_mean_with_weight(
                    previous_value, previous_value_weight, next_value, next_value_weight)

        self.__data = converted
        self.__frames_count = n


    @staticmethod
    def __get_mean_with_weight(a, weight_a, b, weight_b):
        return (a * weight_a + b * weight_b)/(weight_a + weight_b)


    def __convert_reduction(self, n):
        converted = np.array([[0] * self.__coefficients_count] * n, dtype=float)
        to_next_index = n
        last_index = 0
        for i in range(n):

            for _ in range(self.__frames_count):
                if to_next_index == 0:
                    last_index += 1
                    to_next_index = n-1
                else:
                    to_next_index -= 1

                for j in range(self.__coefficients_count):
                    converted[i][j] += self.__data[last_index][j]

            for j in range(self.__coefficients_count):
                converted[i][j] = converted[i][j]/self.__frames_count

        self.__data = converted
        self.__frames_count = n


    def is_equal_to(self, mfcc, float_abs_diff = None):
        """
        Returns true if given mfcc data is equal to this data.\n
        If given data is filled up with float type then float_abs_diff 
        should be specified to use isClose function.
        """
        if self.__coefficients_count != mfcc.__coefficients_count:
            return False
        if self.__frames_count != mfcc.__frames_count:
            return False
        if float_abs_diff is None:
            return (self.__data==mfcc.__data).all()
        for i in range(self.__frames_count):
            for j in range(self.__coefficients_count):
                if not math.isclose(self.__data[i][j], mfcc.__data[i][j], abs_tol=float_abs_diff):
                    return False
        return True


    # TODO Find a better name for this method
    def enlarge_each_cell_to_be_positive(self):
        """
        For given data it changes every value by the difference
        between the smallest value and 0 so the smallest value
        will be 0.\n
        Example:\n
        For given data [[3, -1], [-2, 5]] the result will be
        [[5, 1], [0, 7]]
        """
        if self.__frames_count == 0 or self.__coefficients_count == 0:
            return
        min_val = self.__data.min()
        self.__data = np.array([cell - min_val for cell in [row for row in self.__data]], dtype=float)


    def normalize_to(self, value):
        """
        Multiplies each data to make the sum of the data equal to passed value.
        """
        if self.__frames_count == 0 or self.__coefficients_count == 0:
            return
        ratio = value/math.fabs(self.__data.sum())
        self.__normalize(ratio)


    def __normalize(self, ratio):
        for i in range(self.__frames_count):
            for j in range(self.__coefficients_count):
                self.__data[i][j] = self.__data[i][j] * ratio

    
    def extract_gaussians(self, n_gaussians):
        self.enlarge_each_cell_to_be_positive()
        return em.estimate_n_gaussians_from_mfcc_data(self.__data, n_gaussians)
