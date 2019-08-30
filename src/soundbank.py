import ntpath
import os
import glob

class Soundbank:
    """
    Soundbank gathers all record paths and groups them by phrases.
    Each file is converted into path by cutting the last space.
    'i love spaghetti 3.wav' will be translated into 'i love spaghetti'
    and treated as same phrase with 'i love spaghetti jam.wav'.
    Only WAV files are supported.
    All filenames are converted to lower case.
    """
    def __init__(self, locations):
        self.__records_count = 0
        self.__phrases = dict()
        for location in iter(locations):
            self.__get_record_files_from(location)


    def __get_record_files_from(self, location):
        filenames = self.__get_filepaths_from_directory(location)
        for filename in iter(filenames):
            self.__add_record_to_bank(os.path.join(location, filename))


    def __get_filepaths_from_directory(self, location):
        saved_path = os.getcwd()
        os.chdir(location)
        filenames = glob.glob("*")
        os.chdir(saved_path)
        return filenames


    def __add_record_to_bank(self, filepath):
        name = self.__get_phrase_name_from_file(filepath)
        if name == "":
            return
        self.__records_count += 1
        if name in self.__phrases:
            self.__phrases[name].append(filepath)
        else:
            self.__phrases[name] = [filepath]


    def __get_phrase_name_from_file(self, filepath):
        filename = ntpath.basename(filepath).lower()
        if not filename.endswith(".wav"):
            print("%s is not supported. WAV is the only supported type. Skipping." % filepath)
            return ""
        parts = filename.split(" ")
        return " ".join(parts[:len(parts)-1])

    
    def count_records(self):
        return self.__records_count

    
    def get_phrase_paths(self, phrase):
        return self.__phrases[phrase.lower()]


    def get_phrases(self):
        return self.__phrases.keys()


