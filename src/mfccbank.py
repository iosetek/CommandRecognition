from src.soundbank import Soundbank
from src.mfccphrase import MFCCPhrase
import json

class MFCCBank:
    def __init__(self, mfccphrases):
        self.__phrases = mfccphrases

    
    @classmethod
    def from_soundbank_to_mfccbank(cls, soundbank):
        mfcc_phrases = []
        phrase_names = soundbank.get_phrases()
        print("Converting records to MFCCs! Commands to convert: %d" % len(phrase_names))
        conv_id = 0
        for phrase_name in iter(phrase_names):
            filenames = soundbank.get_phrase_paths(phrase_name)
            print("Converting command: %s. Files to convert: %d" % (phrase_name, len(filenames)))
            mfcc_phrases.append(MFCCPhrase.convert_files_to_mfcc_phrase(phrase_name, filenames))
            conv_id += 1
            print("Converted commands %d/%d" % (conv_id, len(phrase_names)))
        return MFCCBank(mfcc_phrases)


    def remove_silent_frames(self):
        for i in range(len(self.__phrases)):
            self.__phrases[i].remove_silent_frames()


    def discretize_phrases_length(self, step):
        print("Discretizing frames.")
        count_phrases = len(self.__phrases)
        for i in range(count_phrases):
            print("Discretized commands: %d/%d" % (i+1, count_phrases))
            avg_time = self.__phrases[i].average_time()
            self.__phrases[i].convert_to_n_frames(100)
            # self.__phrases[i].convert_to_n_frames(int(round(avg_time/step, 0)))


    def count_phrases(self):
        return len(self.__phrases)


    def get_phrase(self, index):
        return self.__phrases[index]


    @classmethod
    def load_mfccbank(cls, mfccbank_filepath):
        print("Loading from file.")
        file = open(mfccbank_filepath, "r")
        json_str = file.read()
        file.close()
        # TODO Handle that
        obj = json.JSONDecoder().decode(json_str)
        phrases = obj["phrases"]
        parsed_phrases = []
        for phrase in iter(phrases):
            parsed_phrases.append(MFCCPhrase.from_json_object(phrase))
        print("Loaded!")
        return MFCCBank(parsed_phrases)


    def save_mfccbank(self, mfccbank_filepath):
        print("Saving to file.")
        file = open(mfccbank_filepath, "w")
        obj = dict()
        phrases = []
        for p in iter(self.__phrases):
            phrases.append(p.to_json_object())
        obj["phrases"] = phrases
        json_str = json.JSONEncoder().encode(obj)
        file.write(json_str)
        file.close()
        print("Saved!")


    def draw_mfcc_plots(self, destination):
         # TODO
        return 
