from src.command import Command
from src.super_vector import SuperVector
import json

class Model:
    def __init__(self, commands):
        self.__commands = commands

    @classmethod
    def train_model_from_mfccbank(cls, mfccbank, em_gaussians, em_iterations):
        commands = []
        print("Start training!")
        count_phrases = mfccbank.count_phrases()
        print("Commands to train: %d" % count_phrases)
        for i in range(count_phrases):
            commands.append(Command.init_from_mfccphrase(mfccbank.get_phrase(i), em_gaussians, em_iterations))
            print("Trained commands: %d/%d" % (i+1, count_phrases))
        return Model(commands)


    def match(self, record):
        # TODO
        return


    def adapt(self, mfccbank):
        passed = 0
        not_passed = 0

        count = mfccbank.count_phrases()
        for i in range(count):
            phrase = mfccbank.get_phrase(i)
            expected_name = phrase.get_name()
            print("Checking MFCCs for phrase %s" % expected_name)
            mfccs_count = phrase.count_mfccs()
            for m_id in range(mfccs_count):
                mfcc = phrase.get_mfcc(m_id)
                result = self.__match_mfcc(mfcc)
                if expected_name == result:
                    print("Matched correctly!")
                    passed += 1
                else:
                    print("Wrong match!")
                    not_passed += 1
        print("Numbers of checked MFCCs: %d. Matched properly: %d" % (passed + not_passed, passed))


    # TODO: Refactor this. Do not rely on list index or at least make it in separate function.
    def __match_mfcc(self, mfcc):
        sv = SuperVector.init_from_mfcc(mfcc)
        results = []
        for com in iter(self.__commands):
            results.append(com.get_probability_of_this_command(sv.matrix()))

        max_value = max(results)
        # TODO: Watch out for floats!!! :O
        command_id = results.index(max_value)
        return self.__commands[command_id].name


    @classmethod
    def load_from_file(cls, filename):
        print("Loading from file.")
        file = open(filename, "r")
        json_str = file.read()
        file.close()
        # TODO Handle that
        obj = json.JSONDecoder().decode(json_str)
        result = Model(cls.__commands_from_json(obj[Model.__COMMANDS]))
        print("Loaded!")
        return result


    @classmethod
    def __commands_from_json(cls, obj):
        commands = []
        for c in iter(obj):
            commands.append(Command.from_json_obj(c))
        return commands


    def save_to_file(self, filename):
        print("Saving to file.")
        file = open(filename, "w")
        obj = {Model.__COMMANDS: self.__commands_to_json_obj()}
        json_str = json.JSONEncoder().encode(obj)
        file.write(json_str)
        file.close()
        print("Saved!")


    def __commands_to_json_obj(self):
        commands = []
        for c in iter(self.__commands):
            commands.append(c.to_json_obj())
        return commands


    __COMMANDS = "commands"
