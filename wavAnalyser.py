import scipy.io.wavfile as wav
import numpy as np
import math

class Sound:
    def __init__(self, filename: str = None, rate = None, signal = None):
        if filename:
            self.rate, self.signal = wav.read(filename)
        elif rate and signal.any():
            self.rate = rate
            self.signal = signal
        else:
            self.rate = 0
            # TODO: use ndarray constructor to define exactly it.
            self.signal = np.ndarray

    def setRate(self, rate):
        self.rate = rate

    def getRate(self):
        return self.rate

    def getSignal(self):
        return self.signal

    def getSignalMilisecondsFromTo(self, begin, end):
        if begin < 0:
            raise Exception("Cannot get signal from milisecond lower than 0.")
        if end > self.getLength():
            raise Exception("Cannot get signal to milisecond bigger than lenght of the track.")
        startingIndex = self.getIndexAtMilisecond(begin)
        endingIndex = self.getIndexAtMilisecond(end)
        return self.signal[startingIndex:endingIndex]

    def getSignalFromToWithIndex(self, begin, end):
        if begin < 0:
            raise Exception("Cannot get signal from index lower than 0.")
        if end > len(self.signal):
            raise Exception("Cannot get signal to index bigger than lenght of the track.")
        return self.signal[begin:end]

    def getIndexAtMilisecond(self, milisecond):
        """Returns index of signal array which starts current milisecond of track."""
        return math.floor((self.rate/1000)*milisecond)
    
    def getLength(self):
        """Returns length of sound in miliseconds."""
        return int((len(self.signal)/self.rate)*1000)

    def divideIntoArrayOfSounds(self, timestamp):
        """Returns an array of Sound with length less or equal to timestamp (in miliseconds)."""
        sounds = []
        samplesInSingleSound = int((self.rate / 1000) * timestamp)
        repeats = math.ceil(len(self.signal)/samplesInSingleSound)
        for i in range(0, repeats):
            begin = i * samplesInSingleSound
            end = (i+1) * samplesInSingleSound
            if end > len(self.signal):
                end = len(self.signal)
            sounds.append(Sound(rate=self.rate, signal=self.signal[begin : end]))
        return sounds


    def saveToFile(self, filename):
        wav.write(filename, self.rate, self.signal)

    # def getMFCC(self):

