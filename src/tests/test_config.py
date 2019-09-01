from src.config import Config
import unittest


def path_to(file):
    return "/".join(["src/tests/testdata/test_loading_config", file])


class TestConfig(unittest.TestCase):
    def test_invalid_file_form(self):
        with self.assertRaises(Config.InvalidYamlFileException):
            Config(path_to("test_config_with_invalid_structure.yml"))


    def test_missing_field(self):
        with self.assertRaises(Config.MissingParametersException):
            Config(path_to("test_config_missing_parameter.yml"))


    def test_invalid_field(self):
        with self.assertRaises(Config.InvalidParametersException):
            Config(path_to("test_config_invalid_parameter.yml"))


    def test_reading_config(self):
        c = Config(path_to("test_config.yml"))
        self.assertEqual(c.training_paths, ["training_path_a", "training_path_b"])
        self.assertEqual(c.test_paths, ["test_path"])
        self.assertEqual(c.em_repeats, 20)
        self.assertEqual(c.discretization_step, 50)
        self.assertEqual(c.gaussians_count, 2)


