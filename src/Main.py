# from src.gui.ui import Ui

from src.config import Config
from src.soundbank import Soundbank
from src.mfccbank import MFCCBank
from src.model import Model

config = Config("config.yml")
soundbank = Soundbank(config.training_paths)
mfccbank = MFCCBank.from_soundbank_to_mfccbank(soundbank)
mfccbank.remove_silent_frames()
mfccbank.discretize_phrases_length(config.discretization_step)
x = Model.train_model_from_mfccbank(mfccbank, config.gaussians_count, config.em_repeats)
# ui = Ui()

# ui.start()
