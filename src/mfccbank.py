from src.soundbank import Soundbank
from src.mfccphrase import MFCCPhrase

class MFCCBank:
    def __init__(self, mfccphrases):
        self.__phrases = mfccphrases

    
    @classmethod
    def from_soundbank_to_mfccbank(cls, soundbank):
        mfcc_phrases = []
        phrase_names = soundbank.get_phrases()
        for phrase_name in iter(phrase_names):
            filenames = soundbank.get_phrase_paths(phrase_name)
            mfcc_phrases.append(MFCCPhrase.convert_files_to_mfcc_phrase(phrase_name, filenames))
        return MFCCBank(mfcc_phrases)


    def remove_silent_frames(self):
        for i in range(len(self.__phrases)):
            self.__phrases[i].remove_silent_frames()


    def discretize_phrases_length(self, step):
        for i in range(len(self.__phrases)):
            avg_time = self.__phrases[i].average_time()
            self.__phrases[i].convert_to_n_frames(int(round(avg_time/step, 0)))


    def count_phrases(self):
        return len(self.__phrases)


    def get_phrase(self, index):
        return self.__phrases[index]


    @classmethod
    def load_mfccbank(cls, mfccbank_directory):
        # TODO
        return


    def save_mfccbank(self, mfccbank_directory):
        # TODO
        return


    def draw_mfcc_plots(self, destination):
         # TODO
        return


    
