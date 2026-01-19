import asyncio

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QCursor, QGuiApplication
from PySide6.QtWidgets import QApplication, QMessageBox
from qasync import QEventLoop

import toga
from toga.command import Command, Group

from .command import EditOperation
from .libs import create_qapplication
from .screens import Screen as ScreenImpl


def _create_about_dialog(app):
    """
    Qt has an API, namely QMessageBox.about etc, to produce these
    dialogs.  However, these static APIs are blocking and modal, which
    is unlike native apps on KDE where the About dialogs are non-modal.
    """

    message = (
        f'<h2 style="font-weight: normal; margin-bottom: 0px">'
        f"{app.interface.formal_name}</h2>"
    )
    versionauthor = []
    if app.interface.version:
        versionauthor.append(f"Version {app.interface.version}")
    if app.interface.author:
        versionauthor.append(f"Copyright \u00a9 {app.interface.author}")
    if versionauthor != []:
        message += f"<p>{'<br>'.join(versionauthor)}</p>"
    if app.interface.home_page:
        message += (
            f"<p><a href={app.interface.home_page}>{app.interface.home_page}</a></p>"
        )
    dialog = QMessageBox(
        QMessageBox.Information,
        app.interface.formal_name,
        message,
        QMessageBox.NoButton,
        app.get_current_window(),
    )
    icon = dialog.windowIcon()
    dialog.setIconPixmap(icon.pixmap(icon.actualSize(QSize(64, 64))))
    dialog.setModal(False)
    return dialog


class App:
    # Qt apps exit when the last window is closed
    CLOSE_ON_LAST_WINDOW = True
    # Qt apps use default command line handling
    HANDLES_COMMAND_LINE = False

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self

        self.cursorhidden = False
        self._is_exiting = False

        self.native = create_qapplication()
        self.loop = QEventLoop(self.native)
        asyncio.set_event_loop(self.loop)
        self.app_close_event = asyncio.Event()
        # Connect the native signal to an asyncio Event in order
        # for the main event loop to finish running upon app exit
        self.native.aboutToQuit.connect(self.app_close_event.set)
        # Qt does not have a native "applicaction started" signal;
        # however, tasks scheduled on the event loop will only start
        # as soon as the application is running.
        self.loop.call_soon_threadsafe(self.interface._startup)

    ######################################################################
    # Commands and menus
    ######################################################################

    def create_standard_commands(self):
        # On KDE, default bundled apps have the following extra commands,
        # and they automatically enable / disable based on if the associated
        # functionality is available for the current focused widget.
        # There's not a satisfying way to implement that in Qt though...
        # I've referenced https://stackoverflow.com/questions/2047456, so
        # we omit the enabled detection for now.
        # Those KDE bundled apps only have one textfield in the application,
        # so it's trivial for them to implement it.
        self.interface.commands.add(
            Command(
                EditOperation("undo"),
                "Undo",
                shortcut=toga.Key.MOD_1 + "z",
                group=Group.EDIT,
                order=10,
            ),
            Command(
                EditOperation("redo"),
                "Redo",
                shortcut=toga.Key.SHIFT + toga.Key.MOD_1 + "z",
                group=Group.EDIT,
                order=20,
            ),
            Command(
                EditOperation("cut", True),
                "Cut",
                shortcut=toga.Key.MOD_1 + "x",
                group=Group.EDIT,
                section=10,
                order=10,
            ),
            Command(
                EditOperation("copy"),
                "Copy",
                shortcut=toga.Key.MOD_1 + "c",
                group=Group.EDIT,
                section=10,
                order=20,
            ),
            Command(
                EditOperation("paste", True),
                "Paste",
                shortcut=toga.Key.MOD_1 + "v",
                group=Group.EDIT,
                section=10,
                order=30,
            ),
        )

    def create_menus(self):
        for window in self.interface.windows:
            if hasattr(window._impl, "create_menus"):  # pragma: no branch
                window._impl.create_menus()

    ######################################################################
    # App lifecycle
    ######################################################################

    # We can't call this under test conditions, because it would kill the test harness
    def exit(self):  # pragma: no cover
        self._is_exiting = True
        self.native.quit()

    def main_loop(self):
        self.loop.run_until_complete(self.app_close_event.wait())

    def set_icon(self, icon):
        for window in QApplication.topLevelWidgets():
            window.setWindowIcon(icon._impl.native)
        self.interface.commands[Command.ABOUT].icon = icon
        self.interface.commands[Command.PREFERENCES].icon = icon

    def set_main_window(self, window):
        if window == toga.App.BACKGROUND:
            self.native.setQuitOnLastWindowClosed(False)
        else:
            self.native.setQuitOnLastWindowClosed(True)

    ######################################################################
    # App resources
    ######################################################################

    def get_screens(self):
        screens = QGuiApplication.screens()
        primary = QGuiApplication.primaryScreen()
        screens = [primary] + [
            s for s in screens if s != primary
        ]  # Ensure first is primary

        return [ScreenImpl(native=monitor) for monitor in screens]

    ######################################################################
    # App state
    ######################################################################

    def get_dark_mode_state(self):
        return QGuiApplication.styleHints().colorScheme() == Qt.ColorScheme.Dark

    ######################################################################
    # App capabilities
    ######################################################################

    async def _beep(self):
        process = await asyncio.create_subprocess_exec(
            "canberra-gtk-play", "-i", "bell"
        )
        await process.wait()

    def beep(self):
        asyncio.create_task(self._beep())

    def show_about_dialog(self):
        # A reference to the about dialog is stored for facilitate testing.
        # A new instance is created each time to ensure correct window
        # membership.
        self._about_dialog = _create_about_dialog(self)
        self._about_dialog.show()

    ######################################################################
    # Cursor control
    ######################################################################

    def hide_cursor(self):
        if not self.cursorhidden:
            self.cursorhidden = True
            self.native.setOverrideCursor(QCursor(Qt.BlankCursor))

    def show_cursor(self):
        if self.cursorhidden:
            self.cursorhidden = False
            self.native.restoreOverrideCursor()

    ######################################################################
    # Window control
    ######################################################################

    def get_current_window(self):
        return self.native.activeWindow()

    def set_current_window(self, window):
        window._impl.native.activateWindow()
