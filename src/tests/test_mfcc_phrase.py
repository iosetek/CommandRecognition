from src.mfccphrase import MFCCPhrase
from src.mfcc import MFCC
import os
from statistics import mean
import unittest

def get_absolute_path(path):
    prefix = os.getcwd()
    return os.path.join(prefix, "src/tests/testdata/test_mfcc_phrase", path)

class TestEnlargeEachCell(unittest.TestCase):
    def test_mfcc_count(self):
        files = [get_absolute_path("record_a.wav"),
                get_absolute_path("record_b.wav"),
                get_absolute_path("record_c.wav")]
        
        phrase = MFCCPhrase.convert_files_to_mfcc_phrase("test", files)

        self.assertEqual(phrase.count_mfccs(), len(files),
            "Number of MFCCs doesn't match number of records!")


    def test_mfcc_match(self):
        files = [get_absolute_path("record_a.wav"),
                get_absolute_path("record_b.wav")]

        mfccA = MFCC.from_track(files[0])
        mfccB = MFCC.from_track(files[1])

        phrase = MFCCPhrase.convert_files_to_mfcc_phrase("test", files)

        self.assertTrue(mfccA.is_equal_to(phrase.get_mfcc(0)),
            "MFCC from phrase does not match MFCC calculated by original class!")

        self.assertTrue(mfccB.is_equal_to(phrase.get_mfcc(1)),
            "MFCC from phrase does not match MFCC calculated by original class!")

        self.assertFalse(mfccB.is_equal_to(phrase.get_mfcc(0)),
            "MFCC from phrase does matches different MFCC!")

        self.assertFalse(mfccA.is_equal_to(phrase.get_mfcc(1)),
            "MFCC from phrase does matches different MFCC!")



    def test_average_time(self):
        files = [get_absolute_path("record_a.wav"),
                get_absolute_path("record_b.wav"),
                get_absolute_path("record_c.wav")]

        mfccA = MFCC.from_track(files[0])
        mfccB = MFCC.from_track(files[1])
        mfccC = MFCC.from_track(files[2])

        expected_mean = mean([mfccA.count_frames(), mfccB.count_frames(), mfccC.count_frames()])

        phrase = MFCCPhrase.convert_files_to_mfcc_phrase("test", files)

        self.assertEqual(phrase.average_time(), expected_mean,
            "Average time calculated by MFCC Phrase doesn't match with mean from MFCCs!")

        invalid_mean = mean([mfccA.count_frames(), mfccB.count_frames()])

        self.assertNotEqual(phrase.average_time(), invalid_mean,
            "Average time calculated by MFCC Phrase matches with mean from other data!")
