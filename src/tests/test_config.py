from src.config import Config
import unittest


def path_to(file):
    return "/".join(["src/tests/testdata/test_loading_config", file])


class TestConfig(unittest.TestCase):
    def test_config_without_training_records(self):
        with self.assertRaises(Config.MissingTrainingRecordsException):
            Config(path_to("test_config_without_training_records.yml"))

    
    def test_config_without_test_records(self):
        with self.assertRaises(Config.MissingTestRecordsException):
            Config(path_to("test_config_without_test_records.yml"))

    
    def test_config_without_em_repeats(self):
        with self.assertRaises(Config.MissingEMRepeatsException):
            Config(path_to("test_config_without_em_repeats.yml"))

    
    def test_invalid_yaml_structure(self):
        with self.assertRaises(Config.InvalidYamlFileException):
            Config(path_to("test_config_with_invalid_structure.yml"))


    def test_config_without_config(self):
        with self.assertRaises(Config.MissingConfigException):
            Config(path_to("test_config_without_config.yml"))


    def test_config_invalid_training_records_form(self):
        with self.assertRaises(Config.TrainingPathsFieldIsNotListException):
            Config(path_to("test_config_invalid_training_records_form.yml"))


    def test_config_invalid_test_records_form(self):
        with self.assertRaises(Config.TestPathsFieldIsNotListException):
            Config(path_to("test_config_invalid_test_records_form.yml"))


    def test_config_invalid_em_repeats_form(self):
        with self.assertRaises(Config.EMRepeatsFieldIsNotIntigerException):
            Config(path_to("test_config_invalid_em_repeats_form.yml"))


    def test_reading_config(self):
        c = Config("src/tests/testdata/test_loading_config/test_config.yml")
        self.assertEqual(c.training_paths, ["data/commands/tracks", "data/commands/tracks-ania"])
        self.assertEqual(c.test_paths, ["data/commands/test-records"])
        self.assertEqual(c.em_repeats, 20)


