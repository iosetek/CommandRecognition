from .appJar.appjar import gui
from .actions import ActionsUI
from .command import CommandUI
from .help import HelpUI
from .menu import MenuUI
from .model import ModelUI
from .test import TestUI
# from api import Api

class Ui:
    def __init__(self):
        self.__app = gui()

    def start(self):
        self.__prepare_window()
        self.__create_menu()
        self.__app.go()

    def __prepare_window(self):
        self.__app.setTitle("Command Recognition")
        self.__app.setSize("500x500")

    def __create_menu(self):
        self.__app.addMenu("Menu", MenuUI.show)
        self.__app.addMenu("Model", ModelUI.show)
        self.__app.addMenu("Commands", CommandUI.show)
        self.__app.addMenu("Actions", ActionsUI.show)
        self.__app.addMenu("Test", TestUI.show)
        self.__app.addMenu("Help", HelpUI.show)




# app.addLabel("title", "lol")
# app.setLabelBg("title", "red")

# x = app.addListBox("listBox", values=[1, 3, 5])

# app.addNamedButton("Start Recording", "RECORD_START", Api.start_recording)
# app.addNamedButton("Stop Recording", "RECORD_STOP", Api.stop_recording)
# app.addNamedButton("Bake model", "MODEL_CREATE", Api.prepare_model)
# app.addNamedButton("Attach bash instruction to command", "ATTACH_BASH_COMMAND", Api.set_command_action_to_bash)
# app.addNamedButton("Attach executable file to command", "ATTACH_EXE_COMMAND", Api.set_command_action_to_exe_file)
# app.addNamedButton("Attach python file to command", "ATTACH_PY_COMMAND", Api.set_command_action_to_py_file)