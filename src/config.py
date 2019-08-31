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
        if self.__DISCRETIZATION_STEP not in c[self.__CONFIG]:
            raise Config.MissingDiscretizationStepException
        if self.__GAUSSIANS_COUNT not in c[self.__CONFIG]:
            raise Config.MissingGaussiansCountException
        if self.__TRAINING_SUPERVECTORS not in c[self.__CONFIG]:
            raise Config.MissingTrainingSupervectorsException
        if self.__TEST_SUPERVECTORS not in c[self.__CONFIG]:
            raise Config.MissingTestSupervectorsException
        if self.__START_FROM not in c[self.__CONFIG]:
            raise Config.MissingStartFromException


    def __validate_value_types(self, c):
        if not isinstance(c[self.__CONFIG][self.__TRAINING_RECORDS], list):
            raise Config.TrainingPathsFieldIsNotListException
        if not isinstance(c[self.__CONFIG][self.__TEST_RECORDS], list):
            raise Config.TestPathsFieldIsNotListException
        if not isinstance(c[self.__CONFIG][self.__EM_REPEATS], int):
            raise Config.EMRepeatsFieldIsNotIntigerException
        if not isinstance(c[self.__CONFIG][self.__DISCRETIZATION_STEP], int):
            raise Config.DiscretizationStepIsNotIntigerException
        if not isinstance(c[self.__CONFIG][self.__GAUSSIANS_COUNT], int):
            raise Config.GaussiansCountIsNotIntigerException
        if not isinstance(c[self.__CONFIG][self.__TRAINING_SUPERVECTORS], str):
            raise Config.TrainingSupervectorsFieldIsNotStringException
        if not isinstance(c[self.__CONFIG][self.__TEST_SUPERVECTORS], str):
            raise Config.TestSupervectorsFieldIsNotStringException
        if not isinstance(c[self.__CONFIG][self.__START_FROM], str) and \
            not self.__is_proper_start_from(c[self.__CONFIG][self.__START_FROM]):
            raise Config.StartFromFieldIsNotValidException


    def __is_proper_start_from(self, value):
        if value == self.FROM_START and value == self.USE_READY_MFCC_BANK:
            return True
        return False



    def __save_configuration(self, c):
        self.training_paths = c[self.__CONFIG][self.__TRAINING_RECORDS]
        self.test_paths = c[self.__CONFIG][self.__TEST_RECORDS]
        self.em_repeats = c[self.__CONFIG][self.__EM_REPEATS]
        self.discretization_step = c[self.__CONFIG][self.__DISCRETIZATION_STEP]
        self.gaussians_count = c[self.__CONFIG][self.__GAUSSIANS_COUNT]
        self.training_supervectors = c[self.__CONFIG][self.__TRAINING_SUPERVECTORS]
        self.test_supervectors = c[self.__CONFIG][self.__TEST_SUPERVECTORS]
        self.start_from = c[self.__CONFIG][self.__START_FROM]


    __CONFIG = "config"
    __TRAINING_RECORDS = "training_records"
    __TEST_RECORDS = "test_records"
    __EM_REPEATS = "em_repeats"
    __DISCRETIZATION_STEP = "discretization_step"
    __GAUSSIANS_COUNT = "gaussians_count"
    __TRAINING_SUPERVECTORS = "training_supervectors"
    __TEST_SUPERVECTORS = "test_supervectors"
    __START_FROM = "start_from"

    
    FROM_START = "FROM_START"
    USE_READY_MFCC_BANK = "USE_READY_MFCC_BANK"



    class MissingTestRecordsException(Exception):
        pass


    class MissingTrainingRecordsException(Exception):
        pass


    class MissingEMRepeatsException(Exception):
        pass


    class MissingConfigException(Exception):
        pass


    class MissingDiscretizationStepException(Exception):
        pass


    class MissingGaussiansCountException(Exception):
        pass


    class MissingTrainingSupervectorsException(Exception):
        pass


    class MissingTestSupervectorsException(Exception):
        pass


    class MissingStartFromException(Exception):
        pass


    class InvalidYamlFileException(Exception):
        pass


    class TrainingPathsFieldIsNotListException(Exception):
        pass


    class TestPathsFieldIsNotListException(Exception):
        pass


    class EMRepeatsFieldIsNotIntigerException(Exception):
        pass


    class DiscretizationStepIsNotIntigerException(Exception):
        pass


    class GaussiansCountIsNotIntigerException(Exception):
        pass


    class TrainingSupervectorsFieldIsNotStringException(Exception):
        pass


    class TestSupervectorsFieldIsNotStringException(Exception):
        pass


    class StartFromFieldIsNotValidException(Exception):
        pass
