from src.gui.appJar.appjar import gui
from src.api import Api

class TestUI:
    def __init__(self, app):
        self.__app = app
        self.__isRecording = False
        self.__RECORD_BUTTON_NAME = "TEST_START_STOP_RECORD_BUTTON"
        self.__USE_ACTION_CHECKBOX_NAME = "TEST_USE_ACTION_CHECKBOX"

    def append_its_content(self):
        """
        Creates view designed for testing command recognition
        ability of current application. It allows user to record
        it's own voice and informs if any command was detected.
        It can be also used to check if action for current command
        works properly.
        """
        self.__add_recording_button()
        self.__app.addNamedCheckBox("USE \nACTION", self.__USE_ACTION_CHECKBOX_NAME)
        print("TODO")

    def __add_recording_button(self):
        self.__app.addImageButton(
            self.__RECORD_BUTTON_NAME,
            self.__record_button_pressed,
            "src/gui/gfx/button_record_start.gif")
        
    def __record_button_pressed(self):
        if self.__isRecording:
            self.__isRecording = False
            self.__app.setButtonImage(self.__RECORD_BUTTON_NAME, "src/gui/gfx/button_record_start.gif")
            Api.stop_recording()
        else:
            self.__isRecording = True
            self.__app.setButtonImage(self.__RECORD_BUTTON_NAME, "src/gui/gfx/button_record_stop.gif")
            Api.start_recording()
        