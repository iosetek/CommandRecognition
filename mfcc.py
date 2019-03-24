import wavAnalyser
import numpy as np
from python_speech_features import mfcc

class MFCCParser:

    def __init__(self,
        windowFunction = np.hamming, windowLength = 0.03, distanceToNextWindow = 0.01,
        cepstralAmount = 13, filtersAmount = 30,
        FFTsize = 1024,
        appendEnergy = True,
        lowFreq = 0, maxFreq = None,
        preemphFilter = 0.97, cepLifter = 22):

        """
        Creates an object to simple extraction of MFCC from sound track.
        Parameters:
        windowFunction - function for extracting single window from sound track,
            example: numpy.hamming
        windowLength - size of single window measured in miliseconds,
        distanceToNextWindow - the distance to next window measured in miliseconds,
        cepstralAmount - number of cepstral coefficients that are extracted from track and stored in single window,
        filtersAmount - number of MEL filters used for extraction,
        FFTsize - TODO
        appendEnergy - if True the zeroth cepstral coefficient is replaced with the log of the total frame energy,
        lowFreq - the lowest frequency that will be considered in extraction,
        maxFreq - the highest frequency that will be considered in extraction,
        preemphFilter - the power of preemphasis filter. Min: 0, Max: 1,
        cepLifter - the power of lifter that will be added to final cepstral coefficients.
        """

        self.windowFunction = windowFunction
        self.windowLength = windowLength
        self.distanceToNextWindow = distanceToNextWindow
        self.cepstralAmount = cepstralAmount
        self.filtersAmount = filtersAmount
        self.FFTsize = FFTsize
        self.appendEnergy = appendEnergy
        self.lowFreq = lowFreq
        self.maxFreq = maxFreq
        self.preemphFilter = preemphFilter
        self.cepLifter = cepLifter

    def toMFCC(self, s):
        """It returns MFCC of the sound passed as a parameter."""
        return mfcc(
            signal=s.getSignal(),
            samplerate=s.getRate(),
            winlen=self.windowLength,
            winstep=self.distanceToNextWindow,
            numcep=self.cepstralAmount,
            nfilt=self.filtersAmount,
            nfft=self.FFTsize,
            lowfreq=self.lowFreq,
            highfreq=self.maxFreq,
            preemph=self.preemphFilter,
            ceplifter=self.cepLifter,
            appendEnergy=self.appendEnergy,
            winfunc=self.windowFunction)