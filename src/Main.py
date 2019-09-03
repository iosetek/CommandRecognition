# from src.gui.ui import Ui

from src.config import Config
from src.soundbank import Soundbank
from src.mfccbank import MFCCBank
from src.model import Model


def run_system():
    config = Config("config.yml")
    m = prepare_model(config)
    test_model(m, config.test_paths, config)


def prepare_model(config):
    if config.start_from == config.FROM_START:
        mfccbank = __parse_paths(config.training_paths, config)
        mfccbank.save_mfccbank(config.training_supervectors)
    elif config.start_from == config.USE_READY_MFCC_BANK:
        mfccbank = MFCCBank.load_mfccbank(config.training_supervectors)
    model = Model.train_model_from_mfccbank(mfccbank, config.gaussians_count, config.em_repeats)
    model.adapt(mfccbank)
    # TODO: Change location
    model.save_to_file("temporaryfile.json")
    return model


def test_model(model, testingPaths, config):
    mfccbank = __parse_paths(testingPaths, config)
    model.adapt(mfccbank)
    # return results


def __parse_paths(paths, config):
    soundbank = Soundbank(paths)
    mfccbank = MFCCBank.from_soundbank_to_mfccbank(soundbank)
    mfccbank.remove_silent_frames()
    mfccbank.discretize_phrases_length(config.discretization_step)
    return mfccbank


# print("MFCC NAME")
# print(mfccbank.get_phrase(0).get_name())
# model.check_mfcc_for_commands(mfccbank.get_phrase(10).get_mfcc(0))
# ui = Ui()

# ui.start()
