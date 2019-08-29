import yaml


class Config:
    def __init__(self, input_file):
        c = self.__load_config_file(input_file)
        self.__check_if_keys_exist(c)
        self.__validate_value_types(c)
        self.__save_configuration(c)
        

    def __load_config_file(self, input_file):
        with open(input_file, 'r') as stream:
            try:
                c = yaml.safe_load(stream)
            except yaml.YAMLError:
                raise Config.InvalidYamlFileException
        return c

    
    def __check_if_keys_exist(self, c):
        if self.__CONFIG not in c:
            raise Config.MissingConfigException
        if self.__TRAINING_RECORDS not in c[self.__CONFIG]:
            raise Config.MissingTrainingRecordsException
        if self.__TEST_RECORDS not in c[self.__CONFIG]:
            raise Config.MissingTestRecordsException
        if self.__EM_REPEATS not in c[self.__CONFIG]:
            raise Config.MissingEMRepeatsException


    def __validate_value_types(self, c):
        if not isinstance(c[self.__CONFIG][self.__TRAINING_RECORDS], list):
            raise Config.TrainingPathsFieldIsNotListException
        if not isinstance(c[self.__CONFIG][self.__TEST_RECORDS], list):
            raise Config.TestPathsFieldIsNotListException
        if not isinstance(c[self.__CONFIG][self.__EM_REPEATS], int):
            raise Config.EMRepeatsFieldIsNotIntigerException


    def __save_configuration(self, c):
        self.training_paths = c[self.__CONFIG][self.__TRAINING_RECORDS]
        self.test_paths = c[self.__CONFIG][self.__TEST_RECORDS]
        self.em_repeats = c[self.__CONFIG][self.__EM_REPEATS]


    __CONFIG = "config"
    __TRAINING_RECORDS = "training_records"
    __TEST_RECORDS = "test_records"
    __EM_REPEATS = "em_repeats"


    class MissingTestRecordsException(Exception):
        pass


    class MissingTrainingRecordsException(Exception):
        pass


    class MissingEMRepeatsException(Exception):
        pass


    class MissingConfigException(Exception):
        pass


    class InvalidYamlFileException(Exception):
        pass


    class TrainingPathsFieldIsNotListException(Exception):
        pass


    class TestPathsFieldIsNotListException(Exception):
        pass


    class EMRepeatsFieldIsNotIntigerException(Exception):
        pass
