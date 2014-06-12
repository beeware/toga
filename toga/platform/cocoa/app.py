from __future__ import print_function, absolute_import, division

import os
import sys

from .libs import *
from .window import Window



class MainWindow(Window):
    def __init__(self, title=None, position=(100, 100), size=(640, 480)):
        super(MainWindow, self).__init__(title, position, size)

    def on_close(self):
        app = NSApplication.sharedApplication()
        app.terminate_(self._delegate)


class App(object):

    def __init__(self, name, app_id, icon=None):
        self.name = name
        self.app_id = app_id

        self.main_window = MainWindow(name)

        if not icon:
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            icon = os.path.join(root_dir, 'resources', 'tiberius.icns')
        self.icon = NSImage.alloc().initWithContentsOfFile_(get_NSString(icon))

    def _startup(self):
        self._impl = NSApplication.sharedApplication()
        self._impl.setActivationPolicy_(NSApplicationActivationPolicyRegular)

        self._impl.setApplicationIconImage_(self.icon)

        # alert = NSAlert.alloc().init()
        # alert.icon = self.icon
        # alert.runModal()

        app_name = sys.argv[0]

        self.menu = NSMenu.alloc().initWithTitle_(get_NSString('MainMenu'))

        # App menu
        self.app_menuItem = self.menu.addItemWithTitle_action_keyEquivalent_(get_NSString(app_name), None, get_NSString(''))
        submenu = NSMenu.alloc().initWithTitle_(get_NSString(app_name))

        menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            get_NSString('About ' + app_name),
            None,
            get_NSString('')
        )
        submenu.addItem_(menu_item)

        menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            get_NSString('Preferences'),
            None,
            get_NSString('')
        )
        submenu.addItem_(menu_item)

        submenu.addItem_(NSMenuItem.separatorItem())

        menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            get_NSString('Quit ' + app_name),
            get_selector('terminate:'),
            get_NSString("q")
        )
        submenu.addItem_(menu_item)

        self.menu.setSubmenu_forItem_(submenu, self.app_menuItem)

        # Help menu
        self.help_menuItem = self.menu.addItemWithTitle_action_keyEquivalent_(get_NSString('Apple'), None, get_NSString(''))
        submenu = NSMenu.alloc().initWithTitle_(get_NSString('Help'))

        menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            get_NSString('Visit homepage'),
            None,
            get_NSString('')
        )
        submenu.addItem_(menu_item)

        self.menu.setSubmenu_forItem_(submenu, self.help_menuItem)

        # Set the menu for the app.
        self._impl.setMainMenu_(self.menu)

    def main_loop(self):
        self._startup()
        self.main_window.app = self
        self.main_window.show()
        self._impl.activateIgnoringOtherApps_(True)
        self._impl.run()
