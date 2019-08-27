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
        return MFCCBank(phrase_names)


    @classmethod
    def load_mfccbank(cls, mfccbank_directory)
        # TODO
        return


    def save_mfccbank(mfccbank_directory)
        # TODO
        return


    def draw_mfcc_plots(destination)
         # TODO
        return


    
