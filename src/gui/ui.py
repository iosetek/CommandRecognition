from src.gui.actions import ActionsUI
from src.gui.appJar.appjar import gui
from src.gui.command import CommandUI
from src.gui.help import HelpUI
from src.gui.menu import MenuUI
from src.gui.model import ModelUI
from src.gui.test import TestUI
# from api import Api

class Ui:
    def __init__(self):
        self.__app = gui()
        self.__app.setSticky("nesw")
        # self.__app.setStretch("both")
        self.__actions = ActionsUI(self.__app)
        self.__command = CommandUI(self.__app)
        self.__help = HelpUI(self.__app)
        self.__menu = MenuUI(self.__app)
        self.__model = ModelUI(self.__app)
        self.__test = TestUI(self.__app)

    def start(self):
        self.__prepare_window()
        self.__create_menu()
        self.__app.go()

    def __prepare_window(self):
        self.__app.setTitle("Command Recognition")
        self.__app.setSize("640x320")

    def __create_menu(self):
        self.__app.startTabbedFrame("Programm")

        self.__app.startTab("Menu")
        self.__menu.append_its_content()
        self.__app.stopTab()

        self.__app.startTab("Model")
        self.__model.append_its_content()
        self.__app.stopTab()

        self.__app.startTab("Commands")
        self.__command.append_its_content()
        self.__app.stopTab()

        self.__app.startTab("Actions")
        self.__actions.append_its_content()
        self.__app.stopTab()

        self.__app.startTab("Test")
        self.__test.append_its_content()
        self.__app.stopTab()

        self.__app.startTab("Help")
        self.__help.append_its_content()
        self.__app.stopTab()
        self.__app.stopTabbedFrame()

        # print(self.__app)

    # def 




# app.addLabel("title", "lol")
# app.setLabelBg("title", "red")

# x = app.addListBox("listBox", values=[1, 3, 5])

# app.addNamedButton("Start Recording", "RECORD_START", Api.start_recording)
# app.addNamedButton("Stop Recording", "RECORD_STOP", Api.stop_recording)
# app.addNamedButton("Bake model", "MODEL_CREATE", Api.prepare_model)
# app.addNamedButton("Attach bash instruction to command", "ATTACH_BASH_COMMAND", Api.set_command_action_to_bash)
# app.addNamedButton("Attach executable file to command", "ATTACH_EXE_COMMAND", Api.set_command_action_to_exe_file)
# app.addNamedButton("Attach python file to command", "ATTACH_PY_COMMAND", Api.set_command_action_to_py_file)