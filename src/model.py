from src.command import Command

class Model:
    def __init__(self, commands):
        self.__commands = commands

    @classmethod
    def train_model_from_mfccbank(cls, mfccbank, em_gaussians, em_iterations):
        commands = []
        print("Start training!")
        count_phrases = mfccbank.count_phrases()
        print("Commands to train: %d" % count_phrases)
        for i in range(len(count_phrases)):
            commands.append(Command.init_from_mfccphrase(mfccbank.mfccphrase(i), em_gaussians, em_iterations))
            print("Trained commands: %d/%d" % (i+1, count_phrases))


    def match(self, record):
        # TODO
        return