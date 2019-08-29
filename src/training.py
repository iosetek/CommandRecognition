from src.soundbank import Soundbank
from src.mfccbank import MFCCBank

def create_model(records):
    sb = Soundbank(records)
    mb = MFCCBank.from_soundbank_to_mfccbank(sb)
    return