import asyncio
import os
import signal
import sys

try:
    import gi
except ImportError:
    # app.py is the first module that will be imported when you import toga_gtk.
    #
    # If Gtk can't be imported, it may be because we're in a virtualenv,
    # and the system python libraries aren't visible. This can be fixed by
    # creating a symlink into the site-packages
    # Try creating a symlink to the system library location.
    # base_packages_dir is where the packages installed by the package manager
    # can be found.
    # gi_system_install_path is where gi can be found in the packages dir.
    # installer_command is the command the user can run to install gi.
    py_version = "%d.%d" % (sys.version_info.major, sys.version_info.minor)

    if sys.version_info.major == 3:
        if os.path.isdir('/usr/lib64/python%s/site-packages/' % (py_version,)):
            # Fedora
            base_packages_dir = '/usr/lib64/python%s/site-packages/' % (py_version,)
            gi_system_install_path = '/usr/lib64/python%s/site-packages/gi' % (py_version,)
            installer_command = 'dnf install pygobject3 python3-gobject'
        elif os.path.isdir('/usr/lib/python3/dist-packages/'):
            # Ubuntu, Debian
            base_packages_dir = '/usr/lib/python3/dist-packages/'
            gi_system_install_path = '/usr/local/lib/python3/dist-packages/gi'
            installer_command = 'apt-get install python3-gi'
        elif os.path.isdir('/usr/lib/python%s/site-packages/' % (py_version,)):
            # Arch
            base_packages_dir = '/usr/lib/python%s/site-packages/' % (py_version,)
            gi_system_install_path = '/usr/lib/python%s/site-packages/gi' % (py_version,)
            installer_command = 'pacman -S python-gobject'
        else:
            raise RuntimeError("Unable to locate your Python packages dir.")
    else:
        raise RuntimeError("Toga requires Python 3.")

    # Use the location of this package to guide us to
    # the location of the virtualenv.
    gi_symlink_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gi')
    pygtkcompat_symlink_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),  'pygtkcompat')
    cairo_symlink_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),  'cairo')

    if gi_symlink_path == gi_system_install_path:
        # If we're not in a virtualenv, just raise the original import error.
        raise
    else:
        gi_path = os.path.join(base_packages_dir, 'gi')
        pygtkcompat_path = os.path.join(base_packages_dir, 'pygtkcompat')
        cairo_path = os.path.join(base_packages_dir, 'cairo')
        if os.path.exists(gi_path) and os.path.isdir(gi_path):

            # If we can identify the gi library, create a symlink to it.
            try:
                print("Creating symlink (%s & %s) to system GTK+ libraries..." % (gi_symlink_path, pygtkcompat_symlink_path))
                os.symlink(gi_path, gi_symlink_path)
                os.symlink(pygtkcompat_path, pygtkcompat_symlink_path)

                try:
                    print("Creating symlink (%s) to system Cairo libraries..." % cairo_symlink_path)
                    os.symlink(cairo_path, cairo_symlink_path)
                except OSError:
                    # If we can't create the symlink, we'll get an error importing cairo;
                    # report the error at time of use, rather than now.
                    pass

                # The call to os.symlink will return almost immediately,
                # but for some reason, it may not be fully flushed to
                # the file system. One way to fix this is to start
                # the process again. This call to os.execl restarts the
                # program with the same arguments, replacing the original
                # operating system process.
                os.execl(sys.executable, sys.executable, *sys.argv)
            except OSError:
                raise RuntimeError("Unable to automatically create symlink to system Python GTK+ bindings.")
        else:
            raise RuntimeError("Unable to locate the Python GTK+ bindings. Have you run '%s'?" % installer_command)

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib


from toga.command import GROUP_BREAK, SECTION_BREAK, Command
import toga
from .window import Window
from toga import Icon
from toga.handlers import wrapped_handler

import gbulb


class MainWindow(Window):
    _IMPL_CLASS = Gtk.ApplicationWindow

    def on_close(self, widget, data):
        pass


class App:
    """
    Todo:
        * Creation of Menus is not working.
        * Disabling of menu items is not working.
        * App Icon is not showing up
    """
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        gbulb.install(gtk=True)
        self.loop = asyncio.get_event_loop()

        self.create()

    def create(self):
        Icon.app_icon = Icon.load(self.interface.icon, default=Icon.TIBERIUS_ICON)
        # Stimulate the build of the app
        self.native = Gtk.Application(application_id=self.interface.app_id, flags=Gio.ApplicationFlags.FLAGS_NONE)

        # Connect the GTK signal that will cause app startup to occur
        self.native.connect('startup', self.startup)
        self.native.connect('activate', self.activate)
        # self.native.connect('shutdown', self.shutdown)

        self.actions = None

    def startup(self, data=None):
        self.interface.commands.add(
            Command(None, 'About ' + self.interface.name, group=toga.Group.APP),
            Command(None, 'Preferences', group=toga.Group.APP),
            # Quit should always be the last item, in a section on it's own
            Command(lambda s: self.exit(), 'Quit ' + self.interface.name, shortcut='q', group=toga.Group.APP, section=sys.maxsize),
            Command(None, 'Visit homepage', group=toga.Group.HELP)
        )

        self.interface.startup()

        # Create the lookup table of menu items,
        # then force the creation of the menus.
        self._actions = {}
        self.create_menus()
        # self.interface.main_window._impl.create_toolbar()

    def activate(self, data=None):
        pass

    def open_document(self, fileURL):
        '''Add a new document to this app.'''
        print("STUB: If you want to handle opening documents, implement App.open_document(fileURL)")

    def create_menus(self):
        # Only create the menu if the menu item index has been created.
        if hasattr(self, '_actions'):
            self._actions = {}
            menubar = Gio.Menu()
            label = None
            submenu = None
            section = None
            for cmd in self.interface.commands:
                if cmd == GROUP_BREAK:
                    if section:
                        submenu.append_section(None, section)

                    if label == '*':
                        self.native.set_app_menu(submenu)
                    else:
                        menubar.append_submenu(label, submenu)

                    label = None
                    submenu = None
                    section = None
                elif cmd == SECTION_BREAK:
                    submenu.append_section(None, section)
                    section = None

                else:
                    if submenu is None:
                        label = cmd.group.label
                        submenu = Gio.Menu()

                    if section is None:
                        section = Gio.Menu()

                    try:
                        action = self._actions[cmd]
                    except KeyError:
                        cmd_id = "command-%s" % id(cmd)
                        action = Gio.SimpleAction.new(cmd_id, None)
                        if cmd.action:
                            action.connect("activate", wrapped_handler(cmd, cmd.action))
                        cmd._widgets.append(action)
                        self._actions[cmd] = action
                        self.native.add_action(action)

                    # cmd.bind(self.interface.factory).set_enabled(cmd.enabled)

                    item = Gio.MenuItem.new(cmd.label, 'app.' + cmd_id)
                    if cmd.shortcut:
                        item.set_attribute_value('accel', GLib.Variant('s', '<Primary>%s' % cmd.shortcut.upper()))

                        # item.set_attribute_value('accel', GLib.Variant(cmd.shortcut, '<Primary>%s' % cmd.shortcut.upper()))

                    section.append_item(item)

            if section:
                submenu.append_section(None, section)

            if submenu:
                if label == '*':
                    self.native.set_app_menu(submenu)
                else:
                    menubar.append_submenu(label, submenu)

            # Set the menu for the app.
            self.native.set_menubar(menubar)

    def main_loop(self):
        # Modify signal handlers to make sure Ctrl-C is caught and handled.
        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self.loop.run_forever(application=self.native)

    def exit(self):
        self.native.quit()
