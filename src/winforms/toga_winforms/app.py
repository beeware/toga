import os
from typing import List, Text
from collections import OrderedDict
from toga.interface.app import App as AppInterface

from .libs import *
from .window import Window
from .widgets.label import Label
# from .widgets.icon import Icon, TIBERIUS_ICON

"""
According to:
https://msdn.microsoft.com/en-us/library/windows/desktop/ms647553(v=vs.85).aspx
"The system assigns a position value to all items in a menu, including separators."
For this reason I have not assigned Index values to any menu items. -- Bruce Eckel
"""

class MenuBuilder():
    """
    Holds all menu items and creates a new menu via rebuild_menu().
    Allows you to add new items later and produce a new menu.
    Needs a mechanism to allow items to be inserted anywhere, not just appended.
    Also to modify an existing item, or delete an item.
    """

    def __init__(self, menu_items: List = []):
        self.menu_items = OrderedDict()
        for m_item in menu_items:
            self.add(m_item[0], m_item[1], m_item[2])

    @staticmethod
    def menu_item(menu_text, on_click_function):
        "Create a single item on a menu"
        _menu_item = WinForms.MenuItem()
        _menu_item.Text = menu_text
        _menu_item.Click += on_click_function
        # How you assign the Index, in case it's actually necessary:
        # _menu_item.Index = 4
        return _menu_item

    @staticmethod
    def menu(menu_text, menu_items):
        "Create one drop-down menu for the menu bar"
        _menu = WinForms.MenuItem()
        _menu.Text = menu_text
        for item in menu_items:
            _menu.MenuItems.Add(item)
        # How you assign the Index, in case it's actually necessary:
        # _menu.Index = 3
        return _menu

    @staticmethod
    def menu_bar(menus):
        "Assemble the menus into a menu bar"
        _menu_bar = WinForms.MainMenu()
        _menu_bar.MenuItems.AddRange(menus)
        return _menu_bar

    def add(self, menu_name: Text, item_name, item_on_click):
        if menu_name not in self.menu_items:
            self.menu_items[menu_name] = []
        self.menu_items[menu_name].append([item_name, item_on_click])

    def rebuild_menu(self):
        menus = []
        for menu_name in self.menu_items:
            items = [MenuBuilder.menu_item(nm, clk) for nm, clk in self.menu_items[menu_name]]
            menus.append(MenuBuilder.menu(menu_name, items))
        return MenuBuilder.menu_bar(menus)


class MainWindow(Window):
    def __init__(self, title=None, position=(100, 100), size=(640, 480)):
        super(MainWindow, self).__init__(title, position, size)

    def create(self):
        super().create()
        self.menu_builder = MenuBuilder([
            ["&File", "&New", self.file_new_on_click],
            ["&File", "E&xit", self.file_exit_on_click],
            ["&Help", "&About", self.help_about_on_click],
        ])
        self._impl.Menu = self.menu_builder.rebuild_menu()

    def file_new_on_click(self, sender, args):
        print("Stub file new")

    def file_exit_on_click(self, sender, args):
        self.close()

    def help_about_on_click(self, sender, args):
        # The following needs debugging:
        # about_window = AboutWindow()
        # about_window.create()
        # about_window.show()
        print("Stub help about...")


class AboutWindow(Window):
    """
    This is not yet working; leaving it here as breadcrumbs for a future solution.
    """
    def __init__(self, title="About", position=(150, 150), size=(100, 100)):
        super(AboutWindow, self).__init__(title, position, size)

    def create(self):
        super().create()
        self._set_title("About This Program")
        self._set_toolbar([])
        # import pdb; pdb.set_trace()
        self._set_content(Label("Help Content"))


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
