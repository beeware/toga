from functools import partial

from PySide6.QtCore import QEvent, Qt, QTimer
from PySide6.QtGui import QWindowStateChangeEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QWidget

from toga.command import Separator
from toga.constants import WindowState
from toga.types import Position, Size

from .container import Container
from .libs import (
    AnyWithin,  # tests hackery...
    get_is_wayland,
    get_testing,
)
from .screens import Screen as ScreenImpl


def _handle_statechange(impl, changeid):
    current_state = impl.get_window_state()
    if changeid != impl._changeventid:  # not the latest state change
        pass  # handle it after the next state change event is ready to process
    if impl._pending_state_transition:
        if impl._pending_state_transition != current_state:
            impl._apply_state(impl._pending_state_transition)
        else:
            impl._pending_state_transition = None


def process_change(native, event):
    if event.type() == QEvent.WindowStateChange:
        old = event.oldState()
        new = native.windowState()
        if not old & Qt.WindowMinimized and new & Qt.WindowMinimized:
            native.interface.on_hide()
        elif old & Qt.WindowMinimized and not new & Qt.WindowMinimized:
            native.interface.on_show()
        impl = native.impl
        # Handle this later as the states etc may not have been fully realized.
        # I have no idea why 100ms is needed here.
        impl._changeventid += 1
        if get_is_wayland():
            QTimer.singleShot(
                100, partial(_handle_statechange, impl, impl._changeventid)
            )
    elif event.type() == QEvent.ActivationChange:
        if native.isActiveWindow():
            native.interface.on_gain_focus()
        else:
            native.interface.on_lose_focus()


class TogaTLWidget(QWidget):
    def __init__(self, impl, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interface = impl.interface
        self.impl = impl

    def changeEvent(self, event):
        process_change(self, event)
        super().changeEvent(event)


class TogaMainWindow(QMainWindow):
    def __init__(self, impl, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interface = impl.interface
        self.impl = impl

    def changeEvent(self, event):
        process_change(self, event)
        super().changeEvent(event)


def wrap_container(widget, impl):
    wrapper = TogaTLWidget(impl)
    layout = QVBoxLayout(wrapper)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    layout.addWidget(widget)
    return wrapper


class Window:
    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.interface._impl = self
        self.container = Container(on_refresh=self.container_refreshed)
        self.container.native.show()
        self._changeventid = 0

        self.create()

        self._hidden_window_state = None
        self._pending_state_transition = None

        self.native.interface = interface
        self.native.impl = self
        self.native.closeEvent = self.qt_close_event
        self.prog_close = False

        self._in_presentation_mode = False

        self.native.setWindowTitle(title)
        self.native.resize(size[0], size[1])
        if not self.interface.resizable:
            self.native.setFixedSize(size[0], size[1])
        if position is not None:
            self.native.move(position[0], position[1])

        # This does not actually work on KDE!
        # self._set_minimizable(self.interface.minimizable)

        self.native.resizeEvent = self.resizeEvent

    def qt_close_event(self, event):
        if not self.prog_close:
            event.ignore()
            if self.interface.closable:
                # Subtlety: If on_close approves the closing
                # this handler doesn't get called again
                self.interface.on_close()

    def create(self):
        self.native = wrap_container(self.container.native, self)

    # def _set_minimizable(self, enabled):
    #     flags = self.native.windowFlags()
    #     if enabled:
    #         flags |= Qt.WindowMinimizeButtonHint
    #     else:
    #         flags &= ~Qt.WindowMinimizeButtonHint
    #     self.native.setWindowFlags(flags)

    def hide(self):
        # https://forum.qt.io/topic/163064/delayed-window-state-read-after-hide-gives-wrong-results-even-in-x11/
        # Sorta unreliable window state when hidden here, pull our own logic.
        if self._hidden_window_state is None:
            self._hidden_window_state = self.get_window_state(in_progress_state=True)
            self._pending_state_transition = None

        self.native.hide()
        # Ideally we'd love to be able to use showEvent but AFAICT
        # it also gets triggered on deminimization and sometimes even
        # TWICE so it's unreliable.  Hack this around, no way to hide
        # window through system in KDE AFAICT anyways.
        self.interface.on_hide()

    def show(self):
        # Do this bee-fore we show as the docs indicate it'd be applied on show
        # and also to avoid brief flashing / failure to apply
        if self._hidden_window_state is not None:
            self.set_window_state(self._hidden_window_state)
            self._hidden_window_state = None
        self.native.show()
        self.interface.on_show()

    def close(self):
        # OK, this is a bit of a stretch, since
        # this could've been a user-induced close
        # on_closed as well, however this flag
        # is only used for qt_close_event and you
        # can check out the subtlety there.
        self.prog_close = True
        self.native.close()

    def get_title(self):
        return self.native.windowTitle()

    def set_title(self, title):
        self.native.setWindowTitle(title)

    def get_size(self):
        if get_testing():
            # Upstream glitch.  Try making a window, set its size, read it after a sec,
            # it changes by 1 or 2.  Reproducible with 300x200 as the size
            # Ideally we should use pytest.approx; however that doesn't support compar-
            # sions.
            return Size(
                AnyWithin(
                    self.native.size().width() - 2, self.native.size().width() + 2
                ),
                AnyWithin(
                    self.native.size().height() - 2, self.native.size().height() + 2
                ),
            )
        else:
            return Size(
                self.native.size().width(),
                self.native.size().height(),
            )

    def set_size(self, size):
        if not self.interface.resizable:
            self.native.setFixedSize(size[0], size[1])
        self.native.resize(size[0], size[1])

    def resizeEvent(self, event):
        if self.interface.content:
            self.interface.content.refresh()

    def _extra_height(self):
        return self.native.size().height() - self.container.native.size().height()

    def container_refreshed(self, container):
        min_width = self.interface.content.layout.min_width
        min_height = self.interface.content.layout.min_height
        size = self.container.native.size()
        # Calling self.set_size here to trigger logic about fixed size windows.
        if size.width() < min_width and size.height() < min_height:
            self.set_size((min_width, min_height + self._extra_height()))
        elif size.width() < min_width:
            self.set_size((min_width, size.height() + self._extra_height()))
        elif size.height() < min_height:
            self.set_size((size.width(), size.height() + self._extra_height()))
        self.container.native.setMinimumSize(min_width, min_height)

    def get_current_screen(self):
        return ScreenImpl(self.native.screen())

    def get_position(self) -> Position:
        return Position(self.native.pos().x(), self.native.pos().y())

    def set_position(self, position):
        self.native.move(position[0], position[1])

    def set_app(self, app):
        # All windows instantiated belongs to your only QApplication
        # but we need to set the icon
        self.native.setWindowIcon(app.interface.icon._impl.native)

    def get_visible(self):
        return self.native.isVisible()

    # =============== WINDOW STATES ================
    # non-minimizable is not implemented as the minimize button
    # still exists at least when using Breeze theme even if it
    # is hinted away.
    def get_window_state(self, in_progress_state=False):
        # NOTE - MINIMIZED does not round-trip on Wayland
        if self._hidden_window_state:
            return self._hidden_window_state
        if in_progress_state and self._pending_state_transition:
            return self._pending_state_transition
        window_state = self.native.windowState()

        if window_state & Qt.WindowFullScreen:
            if self._in_presentation_mode:
                return WindowState.PRESENTATION
            else:
                return WindowState.FULLSCREEN
        elif window_state & Qt.WindowMaximized:
            return WindowState.MAXIMIZED
        elif window_state & Qt.WindowMinimized:
            return WindowState.MINIMIZED
        else:
            return WindowState.NORMAL

    def set_window_state(self, state):
        if (
            self._hidden_window_state
        ):  # skip all the logic and simply do this on next show if currently hidden
            self._hidden_window_state = state
            return

        if self._pending_state_transition:
            self._pending_state_transition = state
            return

        # print("SET WINDOW STATE")

        # Exit app presentation mode if another window is in it
        if any(
            window.state == WindowState.PRESENTATION and window != self.interface
            for window in self.interface.app.windows
        ):
            self.interface.app.exit_presentation_mode()

        if get_is_wayland():
            self._pending_state_transition = state
        self._apply_state(state)

    def _apply_state(self, state):
        if state is None:
            return

        current_state = self.get_window_state()
        current_native_state = self.native.windowState()
        if current_state == WindowState.MINIMIZED and not get_is_wayland():
            self.native.showNormal()
        if current_state == state:
            self._pending_state_transition = None
            return

        if current_state == WindowState.PRESENTATION:
            self.interface.screen = self._before_presentation_mode_screen
            if hasattr(self.native, "menuBar"):
                self.native.menuBar().show()
            del self._before_presentation_mode_screen
            self._in_presentation_mode = False

        if state == WindowState.MAXIMIZED:
            self.native.showMaximized()

        elif state == WindowState.MINIMIZED:
            print("SHOW MIN")
            if not get_is_wayland():
                self.native.showNormal()
            self.native.showMinimized()

        elif state == WindowState.FULLSCREEN:
            self.native.showFullScreen()
            if current_state == WindowState.PRESENTATION:
                QApplication.sendEvent(
                    self.native, QWindowStateChangeEvent(current_native_state)
                )

        elif state == WindowState.PRESENTATION:
            self._before_presentation_mode_screen = self.interface.screen
            if hasattr(self.native, "menuBar"):
                self.native.menuBar().hide()
            # Do this bee-fore showFullScreen bee-cause
            # showFullScreen might immediately trigger the event
            # and the window state read there might read a non-
            # presentation mode
            self._in_presentation_mode = True
            self.native.showFullScreen()
            if current_state == WindowState.FULLSCREEN:
                QApplication.sendEvent(
                    self.native, QWindowStateChangeEvent(current_native_state)
                )

        else:
            self.native.showNormal()

        QApplication.processEvents()

    # ============== STUB =============

    def get_image_data(self):
        pass

    def set_content(self, widget):
        self.container.content = widget


class MainWindow(Window):
    def create(self):
        self.native = TogaMainWindow(self)
        self.native.setCentralWidget(self.container.native)

    def _submenu(self, group, group_cache):
        try:
            return group_cache[group]
        except KeyError:
            parent_menu = self._submenu(group.parent, group_cache)
            submenu = QMenu(group.text)
            parent_menu.addMenu(submenu)

        group_cache[group] = submenu
        return submenu

    def create_menus(self):
        menubar = self.native.menuBar()
        menubar.clear()

        group_cache = {None: menubar}
        submenu = None
        for cmd in self.interface.app.commands:
            submenu = self._submenu(cmd.group, group_cache)
            if isinstance(cmd, Separator):
                submenu.addSeparator()
            else:
                submenu.addAction(cmd._impl.create_menu_item())

    def create_toolbar(self):
        pass
