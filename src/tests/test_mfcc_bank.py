from src.mfccphrase import MFCCPhrase
from src.mfccbank import MFCCBank
from src.mfcc import MFCC
from src.soundbank import Soundbank
import os
from statistics import mean
import unittest

def get_absolute_path(path):
    prefix = os.getcwd()
    return os.path.join(prefix, "src/tests/testdata/test_mfcc_bank", path)

class TestEnlargeEachCell(unittest.TestCase):
    def test_converting_soundbank_to_mfcc_bank(self):
        locations = [get_absolute_path("a_dir"), get_absolute_path("b_dir")]
        sbank = Soundbank(locations)
        bank_records_count = sbank.count_records()

        mbank = MFCCBank.from_soundbank_to_mfccbank(sbank)
        self.assertTrue(False, "TODO")