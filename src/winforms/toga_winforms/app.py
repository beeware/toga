from .libs import Threading, WinForms
from .window import Window


class MainWindow(Window):
    def on_close(self):
        pass


class App:
    _MAIN_WINDOW_CLASS = MainWindow

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

    def create(self):
        self.native = WinForms.Application

        # self.native.setApplicationIconImage_(self.icon.native)

        # Set the menu for the app.
        # self.native.setMainMenu_(self.menu)

        # Call user code to populate the main window
        self.interface.startup()

    def open_document(self, fileURL):
        '''Add a new document to this app.'''
        print("STUB: If you want to handle opening documents, implement App.open_document(fileURL)")

    def create_menus(self):
        self.interface.factory.not_implemented('App.create_menus()')

    def run_app(self):
        self.create()
        self.native.Run(self.interface.main_window._impl.native)

    def main_loop(self):
        thread = Threading.Thread(Threading.ThreadStart(self.run_app))
        thread.SetApartmentState(Threading.ApartmentState.STA)
        thread.Start()
        thread.Join()

    def exit(self):
        self.interface.factory.not_implemented('App.exit()')
