import os

from toga.interface.app import App as AppInterface

from .libs import *

from .window import Window
# from .widgets.icon import Icon, TIBERIUS_ICON


class MainWindow(Window):
    def __init__(self, title=None, position=(100, 100), size=(640, 480)):
        super(MainWindow, self).__init__(title, position, size)


class App(AppInterface):
    _MAIN_WINDOW_CLASS = MainWindow

    def __init__(self, name, app_id, icon=None, startup=None, document_types=None):
        # Set the icon for the app
        # Icon.app_icon = Icon.load(icon, default=TIBERIUS_ICON)

        super().__init__(
            name=name,
            app_id=app_id,
            icon=None,  # Icon.app_icon,
            startup=startup,
            document_types=document_types
        )

    def _startup(self):
        self._impl = WinForms.Application
        Threading.Thread.CurrentThread.ApartmentState = Threading.ApartmentState.STA

        # self._impl.setApplicationIconImage_(self.icon._impl)

        # Set the menu for the app.
        # self._impl.setMainMenu_(self.menu)

        # Call user code to populate the main window
        self.startup()


    def open_document(self, fileURL):
        '''Add a new document to this app.'''
        print("STUB: If you want to handle opening documents, implement App.open_document(fileURL)")

    def main_loop(self):
        self._startup()
        self._impl.Run(self.main_window._impl)
