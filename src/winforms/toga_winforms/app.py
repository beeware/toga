import os

from .libs import *

from .window import Window
# from .widgets.icon import Icon, TIBERIUS_ICON


class MainWindow(Window):
    pass


class App:
    _MAIN_WINDOW_CLASS = MainWindow

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

    def create(self):
        self.native = WinForms.Application
        Threading.Thread.CurrentThread.ApartmentState = Threading.ApartmentState.STA

        # self.native.setApplicationIconImage_(self.icon.native)

        # Set the menu for the app.
        # self.native.setMainMenu_(self.menu)

        # Call user code to populate the main window
        self.interface.startup()

    def open_document(self, fileURL):
        '''Add a new document to this app.'''
        print("STUB: If you want to handle opening documents, implement App.open_document(fileURL)")

    def main_loop(self):
        self.create()
        self.native.Run(self.interface.main_window._impl.native)
