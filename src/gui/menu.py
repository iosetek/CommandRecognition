from src.api import Api
from src.gui.appJar.appjar import gui

class MenuUI:
    def __init__(self, app):
        self.__app = app

    def append_its_content(self):
        """
        Creates view designed for creating or loading existing applications.
        """
        self.__app.addLabel("MENU_APP_NAME_LABEL", "NAME OF APP",
                                row=1, column=1, rowspan=2, colspan=5)
        self.__app.addEntry("MENU_APP_NAME_ENTRY",
                                row=3, column=1, rowspan=2, colspan=5)
        self.__app.addNamedButton("CREATE APP", "MENU_CREATE_APP_BUTTON", print("TODO"),
                                row=6, column=1, rowspan=2, colspan=12)
        self.__app.addNamedButton("RENAME APP", "MENU_RENAME_APP_BUTTON", print("TODO"),
                                row=9, column=1, rowspan=2, colspan=12)
        self.__app.addNamedButton("LOAD APP", "MENU_LOAD_APP_BUTTON", print("TODO"),
                                row=12, column=1, rowspan=2, colspan=12)
        self.__app.addNamedButton("DELETE APP", "MENU_DELETE_APP_BUTTON", print("TODO"),
                                row=15, column=1, rowspan=2, colspan=12)
        self.__app.addLabel("MENU_APPS_NAMES_LABEL", "APP NAMES",
                                row=1, column=14, rowspan=2, colspan=9)
        self.__app.addListBox("MENU_APP_LISTBOX_BUTTON",
                                row=3, column=14, rowspan=11, colspan=9)
        self.__app.addLabel("MENU_LOG_LABEL", "",
                                row=15, column=14, rowspan=2, colspan=9)

        print("TODO")