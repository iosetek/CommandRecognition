import numpy as np
import math

from python_speech_features import mfcc

import src.wav_analyser

class MFCCParser:
    """
        Creates an object to simple extraction of MFCC from sound track.\n
        Parameters:\n
        windowFunction - function for extracting single window from sound track,\n
            example: numpy.hamming
        windowLength - size of single window measured in seconds,\n
        distanceToNextWindow - the distance to next window measured in seconds,\n
        cepstralAmount - number of cepstral coefficients that are extracted from track and stored in single window,\n
        filtersAmount - number of MEL filters used for extraction,\n
        FFTsize - TODO\n
        appendEnergy - if True the zeroth cepstral coefficient is replaced with the log of the total frame energy,\n
        lowFreq - the lowest frequency that will be considered in extraction,\n
        maxFreq - the highest frequency that will be considered in extraction,\n
        preemphFilter - the power of preemphasis filter. Min: 0, Max: 1,\n
        cepLifter - the power of lifter that will be added to final cepstral coefficients.\n
    """

    def __init__(self,
        window_function = np.hamming, window_length = 0.03, distance_to_next_window = 0.01,
        cepstral_amount = 13, filters_amount = 30,
        fft_size = 1024,
        append_energy = True,
        low_freq = 0, max_freq = None,
        preemph_filter = 0.97, cep_lifter = 22):

        self.window_function = window_function
        self.window_length = window_length
        self.distance_to_next_window = distance_to_next_window
        self.cepstral_amount = cepstral_amount
        self.filters_amount = filters_amount
        self.fft_size = fft_size
        self.append_energy = append_energy
        self.low_freq = low_freq
        self.max_freq = max_freq
        self.preemph_filter = preemph_filter
        self.cep_lifter = cep_lifter

    def to_mfcc(self, s):
        """It returns MFCC of the sound passed as a parameter."""
        return mfcc(
            signal=s.get_signal(),
            samplerate=s.get_rate(),
            winlen=self.window_length,
            winstep=self.distance_to_next_window,
            numcep=self.cepstral_amount,
            nfilt=self.filters_amount,
            nfft=self.fft_size,
            lowfreq=self.low_freq,
            highfreq=self.max_freq,
            preemph=self.preemph_filter,
            ceplifter=self.cep_lifter,
            appendEnergy=self.append_energy,
            winfunc=self.window_function)

    def convert_to_n_frames(self, mfcc, n):
        if len(mfcc) == 0 or len(mfcc) == n:
            return mfcc
        if len(mfcc) > n:
            return self.__convert_reduction(mfcc, n)
        return self.__convert_elongation(mfcc, n)

    def __convert_elongation(self, mfcc, n):
        converted = np.array([[0] * self.cepstral_amount] * n, np.float)
        old_length = len(mfcc)

        for i in range(0, n):
            previous_index = math.floor((i*old_length)/n)
            next_index = previous_index + 1
            
            # TODO: Refactor this!
            # this is a temporary workaround to ignore nextIndex when it's out of bounds.
            if next_index == old_length:
                next_index -= 1

            previous_value_weight = n - ((i*old_length)%n)
            if previous_value_weight > old_length:
                next_value_weight = 0
            else:
                next_value_weight = old_length - previous_value_weight

            for j in range(0, self.cepstral_amount):
                previous_value = mfcc[previous_index][j]
                next_value = mfcc[next_index][j]
                converted[i][j] = self.__get_mean_with_weight(
                    previous_value, previous_value_weight, next_value, next_value_weight)

        return converted

    @staticmethod
    def __get_mean_with_weight(a, weight_a, b, weight_b):
        return (a * weight_a + b * weight_b)/(weight_a + weight_b)

    def __convert_reduction(self, mfcc, n):
        converted = np.array([[0] * self.cepstral_amount] * n, np.float)
        to_next_index = n
        last_index = 0
        old_length = len(mfcc)
        for i in range(0, n):

            for _ in range(0, old_length):
                if to_next_index == 0:
                    last_index += 1
                    to_next_index = n-1
                else:
                    to_next_index -= 1

                for j in range(0, self.cepstral_amount):
                    converted[i][j] += mfcc[last_index][j]

            for j in range(0, self.cepstral_amount):
                converted[i][j] = converted[i][j]/old_length

        return converted

    def get_difference(self, mfcc_a, mfcc_b):
        diff = 0
        for i in range(0, len(mfcc_a)):
            for j in range (0, self.cepstral_amount):
                diff += math.pow(math.fabs(mfcc_a[i][j] - mfcc_b[i][j]), 2)
        return diff

    def normalize_to(self, init_data, value):
        """
        Multiplies each data to make the sum of the data equal to passed value.
        """
        total_sum = self.sum_up(init_data)
        ratio = value/math.fabs(total_sum)
        return self.__normalize(init_data, ratio)

    @staticmethod
    def sum_up(init_data):
        result = 0
        for i in init_data:
            for j in i:
                result += j
        print(result)
        return result

    def __normalize(self, init_data, ratio):
        normalized = np.array([[0] * self.cepstral_amount] * len(init_data), np.float)
        for i in range(0, len(init_data)):
            for j in range(0, self.cepstral_amount):
                normalized[i][j] = int(init_data[i][j] * ratio)
        return normalized

    @staticmethod
    def enlarge_each_cell_to_be_positive(init_data):
        # TODO Find a better name for this method
        min_val = init_data.min()
        return np.array([cell - min_val for cell in [row for row in init_data]])

    @staticmethod
    def convert_to_int(init_data):
        return np.array([cell for cell in [row for row in init_data]], dtype=int)