import yaml


class Config:
    def __init__(self, input_file):
        c = self.__load_config_file(input_file)
        self.__validate_types(c)
        self.__custom_validations(c)
        self.__save_configuration(c)
        

    def __load_config_file(self, input_file):
        with open(input_file, 'r') as stream:
            try:
                c = yaml.safe_load(stream)
            except yaml.YAMLError:
                raise Config.InvalidYamlFileException
        return c

    
    def __validate_types(self, c):
        if self.__CONFIG not in c:
            raise Config.MissingParametersException
        for par in iter(self.__get_parameters()):
            if par[Config.__VALUE] not in c[self.__CONFIG]:
                raise Config.MissingParametersException
            if not isinstance(c[self.__CONFIG][par[Config.__VALUE]], par[Config.__TYPE]):
                raise Config.InvalidParametersException


    def __custom_validations(self, c):
        if not self.__is_proper_start_from(c[self.__CONFIG][self.__START_FROM]):
            raise Config.InvalidParametersException


    def __is_proper_start_from(self, value):
        if value == self.FROM_START or value == self.USE_READY_MFCC_BANK:
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


    def __get_parameters(self):
        return [
            {Config.__VALUE:Config.__TRAINING_RECORDS, Config.__TYPE:list},
            {Config.__VALUE:Config.__TEST_RECORDS, Config.__TYPE:list},
            {Config.__VALUE:Config.__EM_REPEATS, Config.__TYPE:int},
            {Config.__VALUE:Config.__DISCRETIZATION_STEP, Config.__TYPE:int},
            {Config.__VALUE:Config.__GAUSSIANS_COUNT, Config.__TYPE:int},
            {Config.__VALUE:Config.__TRAINING_SUPERVECTORS, Config.__TYPE:str},
            {Config.__VALUE:Config.__TEST_SUPERVECTORS, Config.__TYPE:str},
            {Config.__VALUE:Config.__START_FROM, Config.__TYPE:str}]


    __VALUE = "val"
    __TYPE = "type"

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


    class InvalidYamlFileException(Exception):
        pass


    class MissingParametersException(Exception):
        pass


    class InvalidParametersException(Exception):
        pass