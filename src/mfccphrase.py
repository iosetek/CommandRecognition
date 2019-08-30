from statistics import mean
from src.mfcc import MFCC

class MFCCPhrase:
    def __init__(self, name, mfccs):
        self.__name = name
        self.__mfccs = mfccs
        self.__average_time = self.__calculate_average_time()

    
    def __calculate_average_time(self):
        mfcc_lengths = []
        for mfcc in iter(self.__mfccs):
            mfcc_lengths.append(mfcc.count_frames())
        return mean(mfcc_lengths)


    @classmethod
    def convert_files_to_mfcc_phrase(cls, phrase_name, filenames):
        mfccs = []
        for filename in iter(filenames):
            mfccs.append(MFCC.from_track(filename))
        return MFCCPhrase(phrase_name, mfccs)


    def get_name(self):
        return self.__name


    def average_time(self):
        return self.__average_time


    def count_mfccs(self):
        return len(self.__mfccs)


    def get_mfcc(self, id):
        return self.__mfccs[id]


    def remove_silent_frames(self):
        for i in range(len(self.__mfccs)):
            self.__mfccs[i].remove_silence()


    def convert_to_n_frames(self, n):
        for i in range(len(self.__mfccs)):
            self.__mfccs[i].convert_to_n_frames(n)


    