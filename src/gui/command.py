from src.gui.appJar.appjar import gui
from src.api import Api

class CommandUI:
    def __init__(self, app):
        self.__app = app

    def append_its_content(self):
        """
        Creates view designed for registering new commands or editing
        already existing commands. It allows user to load records from
        disk or recording it directly to programm. Each command is
        translated to set of phonem classes described by already
        registered model.
        """

        self.__app.addLabel("COMMANDS_COMMANDS_NAMES_LABEL", "COMMANDS",
                                row=1, column=1, rowspan=2, colspan=5)
        self.__app.addListBox("COMMANDS_COMMANDS_LISTBOX",
                                row=3, column=1, rowspan=7, colspan=5)
        self.__app.addNamedButton("ADD NEW", "COMMANDS_NEW_COMMAND_BUTTON", print("TODO"),
                                row=10, column=1, rowspan=2, colspan=5)
        self.__app.addNamedButton("EDIT", "COMMANDS_EDIT_COMMAND_BUTTON", print("TODO"),
                                row=13, column=1, rowspan=2, colspan=5)
        self.__app.addNamedButton("DELETE", "COMMANDS_DELETE_COMMAND_BUTTON", print("TODO"),
                                row=15, column=1, rowspan=2, colspan=5)

        self.__app.addLabel("COMMANDS_COMMAND_NAME_LABEL", "NAME",
                                row=1, column=6, rowspan=1, colspan=6)
        self.__app.addEntry("COMMANDS_COMMAND_NAME_ENTRY",
                                row=2, column=6, rowspan=1, colspan=2)
        self.__app.addNamedButton("ACTIVATE", "COMMANDS_ACTIVATE_BUTTON", print("TODO"),
                                row=3, column=6, rowspan=1, colspan=6)
        self.__app.addNamedButton("DEACTIVATE", "COMMANDS_DEACTIVATE_BUTTON", print("TODO"),
                                row=4, column=6, rowspan=1, colspan=6)
        self.__app.addNamedButton("CALCULATE", "COMMANDS_CALCULATE_BUTTON", print("TODO"),
                                row=5, column=6, rowspan=1, colspan=6)
        self.__app.addLabel("COMMANDS_LOG_LABEL", "",
                                row=6, column=6, rowspan=1, colspan=14)

        self.__app.addLabel("COMMANDS_RECORDS_NAMES_LABEL", "RECORDS",
                                row=1, column=12, rowspan=2, colspan=7)
        self.__app.addListBox("COMMANDS_RECORD_LISTBOX",
                                row=3, column=12, rowspan=5, colspan=7)
        self.__app.addNamedButton("PLAY", "COMMANDS_PLAY_RECORD_BUTTON", print("TODO"),
                                row=9, column=12, rowspan=2, colspan=3)
        self.__app.addNamedButton("DELETE", "COMMANDS_DELETE_RECORD_BUTTON", print("TODO"),
                                row=9, column=15, rowspan=2, colspan=4)
        self.__app.addNamedButton("RECORD NEW", "COMMANDS_RECORD_RECORD_BUTTON", print("TODO"),
                                row=11, column=12, rowspan=2, colspan=7)
        self.__app.addNamedButton("LOAD", "COMMANDS_LOAD_RECORD_BUTTON", print("TODO"),
                                row=13, column=12, rowspan=2, colspan=7)

        print("TODO")