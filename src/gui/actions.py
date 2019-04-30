from src.api import Api
from src.gui.appJar.appjar import gui


class ActionsUI:
    def __init__(self, app):
        self.__app = app

    def append_its_content(self):
        """
        Creates view designed to create action and attach it to
        particular command. Action can be defined as executing
        executable file, python file or using list of bash commands.
        """

        self.__app.addListBox("ACTIONS_COMMAND_LISTBOX",
                                row=1, column=1, rowspan=8, colspan=5)
        self.__app.addNamedButton("ATTACH COMMAND", "ACTIONS_ATTACH_COMMAND", print("TODO"),
                                row=10, column=1, rowspan=2, colspan=5)
        self.__app.addNamedButton("DETACH COMMAND", "ACTIONS_DETACH_COMMAND", print("TODO"),
                                row=13, column=1, rowspan=2, colspan=5)

        self.__app.addListBox("ACTIONS_ACTION_LISTBOX",
                                row=1, column=7, rowspan=5, colspan=5)
        self.__app.addNamedButton("NEW COMMAND", "ACTIONS_NEW_COMMAND", print("TODO"),
                                row=7, column=7, rowspan=2, colspan=5)
        self.__app.addNamedButton("EDIT COMMAND", "ACTIONS_EDIT_COMMAND", print("TODO"),
                                row=10, column=7, rowspan=2, colspan=5)
        self.__app.addNamedButton("REMOVE COMMAND", "ACTIONS_REMOVE_COMMAND", print("TODO"),
                                row=13, column=7, rowspan=2, colspan=5)
        
        self.__app.addLabel("ACTIONS_ACTION_NAME_LABEL", "ACTION NAME",
                                row=2, column=13, rowspan=2, colspan=9)
        self.__app.addEntry("ACTIONS_ACTION_NAME_ENTRY",
                                row=4, column=13, rowspan=2, colspan=9)
        self.__app.addNamedButton("SET EXE FILE", "ACTIONS_SET_EXE_FILE_BUTTON", print("TODO"),
                                row=7, column=13, rowspan=2, colspan=9)
        self.__app.addNamedButton("SET PYTHON FILE", "ACTIONS_SET_PY_FILE_BUTTON", print("TODO"),
                                row=10, column=13, rowspan=2, colspan=9)
        self.__app.addNamedButton("SET BASH COMMAND", "ACTIONS_SET_BASH_COMMAND_BUTTON", print("TODO"),
                                row=13, column=13, rowspan=2, colspan=9)

        print("TODO")