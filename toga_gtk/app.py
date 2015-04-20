from __future__ import print_function, absolute_import, division

import signal
import sys

try:
    from gi.repository import Gtk, Gio, GLib
except ImportError:
    # app.py is the first module that will be imported when you import toga_gtk.
    #
    # If Gtk can't be imported, it may be because we're in a virtualenv,
    # and the system python libraries aren't visible. This can be fixed by
    # creating a symlink into the site-packages
    # Try creating a symlink to the system library location.
    # gi_path is the location of the system install of the gi library
    # package_name is the package to 'apt-get install'
    # symlink_path is the full name of the symlink to create.
    import os
    if sys.version_info.major == 3:
        package_name = 'python-gi'
        gi_path = '/usr/lib/python3/dist-packages/gi'
        system_packages_path = '/usr/local/lib/python3/dist-packages/gi'
    else:
        package_name = 'python3-gi'
        gi_path = '/usr/lib/python2.7/dist-packages/gi'
        system_packages_path = '/usr/local/lib/python2.7/dist-packages/gi'

    # Use the location of this package to guide us to
    # the location of the virtualenv.
    symlink_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gi')

    if symlink_path == system_packages_path:
        # If we're not in a virtualenv, just raise the original import error.
        raise
    else:
        if os.path.exists(gi_path) and os.path.isdir(gi_path):
            # If we can identify the gi library, create a symlink to it.
            try:
                print ("Creating symlink (%s) to system GTK+ libraries..." % symlink_path)
                os.symlink(gi_path, symlink_path)

                from gi.repository import Gtk, Gio, GLib
            except OSError:
                raise RuntimeError("Unable to automatically create symlink to system Python GTK+ bindings.")
        else:
            raise RuntimeError("Unable to locate the Python GTK+ bindings. Have you run 'apt-get install %s'?" % package_name)

from .window import Window
from .widgets.icon import Icon, TIBERIUS_ICON


class MainWindow(Window):
    _IMPL_CLASS = Gtk.ApplicationWindow


class App(object):

    def __init__(self, name, app_id, icon=None, startup=None):
        # GLib.set_application_name(name.encode('ascii'))
        self._impl = Gtk.Application(application_id=app_id, flags=Gio.ApplicationFlags.FLAGS_NONE)

        # Set the icon for the app
        Icon.app_icon = Icon.load(icon, default=TIBERIUS_ICON)
        self.icon = Icon.app_icon

        self._startup_method = startup

        # Connect the GTK signal that will cause app startup to occur
        self._impl.connect('startup', self._startup)
        self._impl.connect('activate', self._activate)
        # self._impl.connect('shutdown', self._shutdown)

    def _startup(self, data=None):
        self.main_window = MainWindow()

        self.main_window.app = self

        self._impl.add_window(self.main_window._impl)

        action = Gio.SimpleAction.new('stuff', None)
        action.connect('activate', self._quit)
        self._impl.add_action(action)

        app_name = sys.argv[0]

        # # App menu
        self.app_menu = Gio.Menu()

        section = Gio.Menu()
        section.append_item(Gio.MenuItem.new('About', 'about'))
        section.append_item(Gio.MenuItem.new('Preferences', 'preferences'))

        self.app_menu.append_section(None, section)

        section = Gio.Menu()
        item = Gio.MenuItem.new('Do Stuff', 'app.stuff')
        item.set_attribute_value('accel', GLib.Variant('s', '<Primary>S'))
        section.append_item(item)

        self.app_menu.append_section(None, section)

        self._impl.set_app_menu(self.app_menu)

        # # Main menu bar
        self.menu_bar = Gio.Menu()

        # FIXME - the app menu doesn't display correctly - it assumes a title of
        # "Unknown application name", which doesn't appear to be changeable, and may
        # be an ubuntu unity bug...
        # self.menu_bar.append_submenu('File', self.app_menu)

        # Help
        submenu = Gio.Menu()

        section = Gio.Menu()
        section.append_item(Gio.MenuItem.new('Help', 'help'))

        submenu.append_section(None, section)

        self.menu_bar.append_submenu('Help', submenu)

        self._impl.set_menubar(self.menu_bar)

        self.startup()

        self.main_window.show()

    def startup(self):
        if self._startup_method:
            self.main_window.content = self._startup_method(self)

    def _activate(self, data=None):
        pass

    def main_loop(self):

        # Modify signal handlers to make sure Ctrl-C is caught and handled.
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self._impl.run(None)

    def _quit(self, widget, data=None):
        self.on_quit()

    def on_quit(self):
        self._impl.quit()
