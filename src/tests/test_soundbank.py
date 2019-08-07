import unittest
import numpy as np
import os
import math
from src.soundbank import Soundbank

def get_absolute_path(path):
    prefix = os.getcwd()
    return os.path.join(prefix, "src/tests/testdata/test_soundbank", path)

class TestEnlargeEachCell(unittest.TestCase):
    def test_uppercase_lowercase(self):
        locations = [get_absolute_path("uppercase_lowercase")]
        bank = Soundbank(locations)
        all_records_count = bank.count_records()
        test_phrase_count = len(bank.get_phrase_paths("test"))

        self.assertEqual(all_records_count, 4, "Invalid number of records!")
        self.assertEqual(test_phrase_count, 4, "Not enough 'test' phrase records!")

    def test_other_phrases(self):
        locations = [get_absolute_path("other_phrases")]
        bank = Soundbank(locations)
        all_records_count = bank.count_records()
        test_phrase_count = len(bank.get_phrase_paths("test"))
        test_x_phrase_count = len(bank.get_phrase_paths("testX"))
        other_test_phrase_count = len(bank.get_phrase_paths("other test"))
        
        self.assertEqual(all_records_count, 12, "Invalid number of records!")
        self.assertEqual(test_phrase_count, 4, "Not enough 'test' phrase records!")
        self.assertEqual(test_x_phrase_count, 5, "Not enough 'testX' phrase records!")
        self.assertEqual(other_test_phrase_count, 3, "Not enough 'other test' phrase records!")

    def test_not_wav_files(self):
        locations = [get_absolute_path("not_wav_files")]
        bank = Soundbank(locations)
        all_records_count = bank.count_records()
        test_phrase_count = len(bank.get_phrase_paths("test"))
        
        self.assertEqual(all_records_count, 1, "Invalid number of records!")
        self.assertEqual(test_phrase_count, 1, "Not enough 'test' phrase records!")

    def test_different_suffixes(self):
        locations = [get_absolute_path("different_suffixes")]
        bank = Soundbank(locations)
        all_records_count = bank.count_records()
        test_phrase_count = len(bank.get_phrase_paths("test"))
        
        self.assertEqual(all_records_count, 4, "Invalid number of records!")
        self.assertEqual(test_phrase_count, 4, "Not enough 'test' phrase records!")

    def test_multiple_directories(self):
        locations = [get_absolute_path("multiple_directories/dir_a"),
                get_absolute_path("multiple_directories/dir_b"),
                get_absolute_path("multiple_directories/dir_c")]
        bank = Soundbank(locations)
        all_records_count = bank.count_records()
        test_phrase_count = len(bank.get_phrase_paths("test"))
        test_x_phrase_count = len(bank.get_phrase_paths("testX"))
        other_test_phrase_count = len(bank.get_phrase_paths("other test"))
        
        self.assertEqual(all_records_count, 12, "Invalid number of records!")
        self.assertEqual(test_phrase_count, 3, "Not enough 'test' phrase records!")
        self.assertEqual(test_x_phrase_count, 4, "Not enough 'testX' phrase records!")
        self.assertEqual(other_test_phrase_count, 5, "Not enough 'other test' phrase records!")

    