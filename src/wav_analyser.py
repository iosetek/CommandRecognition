import scipy.io.wavfile as wav
import numpy as np
import math

class Sound:
    def __init__(self, filename = None, rate = None, signal = None):
        if filename:
            self.rate, self.signal = wav.read(filename)
        elif rate and signal.any():
            self.rate = rate
            self.signal = signal
        else:
            self.rate = 0
            # TODO: use ndarray constructor to define exactly it.
            self.signal = np.ndarray

    def set_rate(self, rate):
        self.rate = rate

    def get_rate(self):
        return self.rate

    def get_signal(self):
        return self.signal

    def get_signal_miliseconds_from_to(self, begin, end):
        if begin < 0:
            raise Exception("Cannot get signal from milisecond lower than 0.")
        if end > self.get_length():
            raise Exception("Cannot get signal to milisecond bigger than lenght of the track.")
        starting_index = self.get_index_at_milisecond(begin)
        ending_index = self.get_index_at_milisecond(end)
        return self.signal[starting_index:ending_index]

    def get_signal_from_to_with_index(self, begin, end):
        if begin < 0:
            raise Exception("Cannot get signal from index lower than 0.")
        if end > len(self.signal):
            raise Exception("Cannot get signal to index bigger than lenght of the track.")
        return self.signal[begin:end]

    def get_index_at_milisecond(self, milisecond):
        """Returns index of signal array which starts current milisecond of track."""
        return math.floor((self.rate/1000)*milisecond)
    
    def get_length(self):
        """Returns length of sound in miliseconds."""
        return int((len(self.signal)/self.rate)*1000)

    def divide_into_array_of_sounds(self, timestamp):
        """Returns an array of Sound with length less or equal to timestamp (in miliseconds)."""
        sounds = []
        samples_in_single_sound = int((self.rate / 1000) * timestamp)
        repeats = math.ceil(len(self.signal)/samples_in_single_sound)
        for i in range(repeats):
            begin = i * samples_in_single_sound
            end = (i+1) * samples_in_single_sound
            if end > len(self.signal):
                end = len(self.signal)
            sounds.append(Sound(rate=self.rate, signal=self.signal[begin : end]))
        return sounds


    def saveToFile(self, filename):
        wav.write(filename, self.rate, self.signal)

    # def getMFCC(self):

