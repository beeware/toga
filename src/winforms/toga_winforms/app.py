import os

from toga.interface.app import App as AppInterface

from .libs import *

from .window import Window
# from .widgets.icon import Icon, TIBERIUS_ICON
"""
According to:
https://msdn.microsoft.com/en-us/library/windows/desktop/ms647553(v=vs.85).aspx
"The system assigns a position value to all items in a menu, including separators."
For this reason I have not assigned Index values to any menu items. -- Bruce Eckel
"""

def menu_item(menu_text, on_click_function):
    "Create a single item on a menu"
    _menu_item = WinForms.MenuItem()
    _menu_item.Text = menu_text
    _menu_item.Click += on_click_function
    # How you assign the Index, in case it's actually necessary:
    # _menu_item.Index = 4
    return _menu_item

def menu(menu_text, menu_items):
    "Create one drop-down menu for the menu bar"
    _menu = WinForms.MenuItem()
    _menu.Text = menu_text
    for item in menu_items:
        _menu.MenuItems.Add(item)
    # How you assign the Index, in case it's actually necessary:
    # _menu.Index = 3
    return _menu

def menu_bar(menus):
    "Assemble the menus into a menu bar"
    _menu_bar = WinForms.MainMenu()
    _menu_bar.MenuItems.AddRange(menus)
    return _menu_bar


class MainWindow(Window):
    def __init__(self, title=None, position=(100, 100), size=(640, 480)):
        super(MainWindow, self).__init__(title, position, size)

    def create(self):
        super().create()
        self._impl.Menu = menu_bar((
            # Add more menus as needed:
            menu("&File", (
                # Add more menu_items as needed:
                menu_item("&New", self.file_new_on_click),
                menu_item("&Exit", self.file_exit_on_click),
            )),
            menu("&Help", (
                menu_item("&About", self.help_about_on_click),
            )),
        ))

    def file_new_on_click(self, sender, args):
        print("Stub file new")

    def file_exit_on_click(self, sender, args):
        self.close()

    def help_about_on_click(self, sender, args):
        print("Stub help about...")


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

        # Call user code to populate the main window
        self.startup()

    def open_document(self, fileURL):
        '''Add a new document to this app.'''
        print("STUB: If you want to handle opening documents, implement App.open_document(fileURL)")

    def main_loop(self):
        self._startup()
        self._impl.Run(self.main_window._impl)
