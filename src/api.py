import glob, os

class Api:
    @staticmethod
    def load_command_lists():
        """
        Returns list of existing directories within data/commands directory.
        """
        saved_path = os.getcwd()
        Api.__ensure_command_directory_exists()
        os.chdir("data/commands")
        directories = Api.__get_directories()
        os.chdir(saved_path)
        return directories


    @staticmethod
    def __ensure_command_directory_exists():
        if not os.path.isdir("data"):
            os.mkdir("data")

        if not os.path.isdir("data/commands"):
            os.mkdir("data/commands")


    @staticmethod
    def __get_directories():
        files = glob.glob("**")
        directories = []
        for file in files:
            if os.path.isdir(file):
                directories.append(file)
        return directories

    @staticmethod
    def load_commands(list_name):
        """
        Returns registered commands from directory name
        specified as list_name from data/commands directory.
        """
        saved_path = os.getcwd()
        Api.__ensure_command_directory_exists()
        # if not os.path.isdir("data"):

    @staticmethod
    def prepare_model(name):
        """
        Translates a bunch of base commands and turns them into phonem classes.
        """
        print("TODO")

    @staticmethod
    def load_model(name):
        """
        Load one of registered models and use it to register a new command.
        """
        print("TODO")


    @staticmethod
    def load_model_names():
        """
        Get names of existing registered models.
        """
        print("TODO")


    @staticmethod
    def start_recording():
        """
        Start collecting data from microphone.
        """
        print("TODO")

    @staticmethod
    def stop_recording():
        """
        Stop collecting data from microphone and keep it.
        """
        print("TODO")

    @staticmethod
    def save_record():
        """
        Save record to file.
        """
        print("TODO")


    @staticmethod
    def set_command_action_to_bash(action):
        """
        Attach bash command to actual command.
        """
        print("TODO")


    @staticmethod
    def set_command_action_to_py_file(file):
        """
        Attach executable file to actual command.
        """
        print("TODO")


    @staticmethod
    def set_command_action_to_exe_file(file):
        """
        Attach python file to actual command.
        """
        print("TODO")


    @staticmethod
    def create_application():
        """
        Create new python application that listens for given commands
        and realizes actions attached to them if it detects any of them.
        """
        print("TODO")


    