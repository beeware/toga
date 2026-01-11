from functools import partial

from PySide6.QtCore import QBuffer, QEvent, QIODevice, Qt, QTimer
from PySide6.QtGui import QAction, QResizeEvent, QWindowStateChangeEvent
from PySide6.QtWidgets import QApplication, QMainWindow, QMenu, QToolBar

from toga.command import Separator
from toga.constants import WindowState
from toga.types import Position, Size

from .container import Container
from .libs import (
    IS_WAYLAND,
)
from .screens import Screen as ScreenImpl


class TogaMainWindow(QMainWindow):
    def __init__(self, impl, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interface = impl.interface
        self.impl = impl

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            old = event.oldState()
            new = self.windowState()
            # Those branches cannot be triggered reliably on Wayland, as
            # Minimized is not a reliable window state.
            if (  # pragma: no-cover-if-linux-wayland
                not old & Qt.WindowMinimized and new & Qt.WindowMinimized
            ):
                self.interface.on_hide()
            elif (  # pragma: no-cover-if-linux-wayland
                old & Qt.WindowMinimized and not new & Qt.WindowMinimized
            ):
                self.interface.on_show()

            if IS_WAYLAND:  # pragma: no-cover-if-linux-x  # pragma: no branch
                # Hold clearing _pending_state_transition by 100ms to ensure that
                # any window state changes in the meantime get batched.
                impl = self.impl
                impl._state_lock = True
                impl._changeeventid += 1
                QTimer.singleShot(
                    100, partial(impl._clear_pending, impl._changeeventid)
                )
        elif event.type() == QEvent.ActivationChange:
            if self.isActiveWindow():
                self.interface.on_gain_focus()
            else:
                self.interface.on_lose_focus()
        super().changeEvent(event)


class Window:
    def _clear_pending(self, changeeventid):  # pragma: no-cover-if-linux-x
        if self._changeeventid != changeeventid:
            return
        if self._pending_state_transition:
            self._apply_state(self._pending_state_transition)
            self._pending_state_transition = None
        self._state_lock = False

    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.interface._impl = self
        self.container = Container(on_refresh=self.content_refreshed)
        self.container.native.show()
        self._changeeventid = 0

        self.create()

        self._hidden_window_state = None
        self._pending_state_transition = None
        self._state_lock = False

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

        # Note:  KDE's default theme does not respond to minimize button
        # window hints, so minimizable cannot be implemented.

        self.container.native.resizeEvent = self.resizeEvent
        self.toolbar_native = None

    def qt_close_event(self, event):
        if not self.prog_close:
            # Subtlety: If on_close approves the closing
            # this handler doesn't get called again.  Therefore
            # the event is always rejected.
            event.ignore()
            if self.interface.closable:
                self.interface.on_close()

    def create(self):
        # QMainWindow is used in order to save duplication for
        # subclassing;  QMainWindow does not *require* a menubar,
        # and if there are no items, it is not displayed.
        # This also allows us to simplify menubar hiding logic
        # by not requiring us to check hasattr.
        self.native = TogaMainWindow(self)
        self.native.setCentralWidget(self.container.native)

    def hide(self):
        # https://forum.qt.io/topic/163064/delayed-window-state-read-after-hide-gives-wrong-results-even-in-x11/
        # The window state when a window is hidden is unreliable in
        # regards to preserving normal vs. maximized state, so caching
        # is done for window states when the window is hidden.
        self._hidden_window_state = self.get_window_state(in_progress_state=True)
        self._pending_state_transition = None

        self.native.hide()
        # Ideally, showEvent and hideEvent should be used on Qt; however,
        # due to some unknown subtleties to me, these events are unreliable
        # and sometimes emits multiple times during window state changes;
        # therefore, emit on_hide here, on_show when programmatically showing,
        # and use the window state change events to handle show/hide from
        # window states, since there isn't a way to hide windows by the user
        # as far as I know of on KDE.
        self.interface.on_hide()

    def show(self):
        # Restore cached state before we show as the docs indicate that window states
        # set when a window is hidden will be applied on show, to avoid any brief
        # flashing or failure to apply.
        if self._hidden_window_state is not None:
            self.set_window_state(self._hidden_window_state)
            self._hidden_window_state = None
        self.native.show()
        self.interface.on_show()

    def close(self):
        self.prog_close = True
        self.native.close()

    def get_title(self):
        return self.native.windowTitle()

    def set_title(self, title):
        self.native.setWindowTitle(title)

    def get_size(self):
        return Size(
            self.native.size().width(),
            self.native.size().height(),
        )

    def set_size(self, size):
        self.native.resize(size[0], size[1])

    def resizeEvent(self, event):
        self.interface.on_resize()
        if self.interface.content:
            self.interface.content.refresh()

    def content_refreshed(self, container):
        min_width = self.interface.content.layout.min_width
        min_height = self.interface.content.layout.min_height
        self.container.native.setMinimumSize(min_width, min_height)
        self.container.min_width = min_width
        self.container.min_height = min_height

    def get_current_screen(self):
        return ScreenImpl(self.native.screen())

    def get_position(self) -> Position:
        return Position(self.native.pos().x(), self.native.pos().y())

    def set_position(self, position):
        self.native.move(position[0], position[1])

    def set_app(self, app):
        # All windows instantiated belongs to your only QApplication
        # and no need to explicitly set app, but the app icon needs to be
        # applied onto the window.
        self.native.setWindowIcon(app.interface.icon._impl.native)

    def get_visible(self):
        return self.native.isVisible()

    # =============== WINDOW STATES ================
    def get_window_state(self, in_progress_state=False):
        if self._hidden_window_state:
            return self._hidden_window_state
        # The following is no-covered because it has became an
        # implementation detail only used by saving window state
        # when hidden and a window state is in transition, and to
        # stay consistency with the other backends providing
        # this impl API.  This functionality is also relatively
        # minor.
        if in_progress_state and self._pending_state_transition:  # pragma: no cover
            return self._pending_state_transition
        window_state = self.native.windowState()

        if window_state & Qt.WindowFullScreen:
            if self._in_presentation_mode:
                return WindowState.PRESENTATION
            else:
                return WindowState.FULLSCREEN
        elif window_state & Qt.WindowMaximized:
            return WindowState.MAXIMIZED
        elif window_state & Qt.WindowMinimized:  # pragma: no-cover-if-linux-wayland
            return WindowState.MINIMIZED
        else:
            return WindowState.NORMAL

    def set_window_state(self, state):
        if self._state_lock:  # pragma: no-cover-if-linux-x
            self._pending_state_transition = state
            return

        # Exit app presentation mode if another window is in it
        if any(
            window.state == WindowState.PRESENTATION and window != self.interface
            for window in self.interface.app.windows
        ):
            self.interface.app.exit_presentation_mode()

        if IS_WAYLAND:  # pragma: no-cover-if-linux-x  # pragma: no branch
            # Hold clearing _pending_state_transition by 100ms to ensure that
            # any window state changes in the meantime get batched.
            self._state_lock = True
            self._changeeventid += 1
            QTimer.singleShot(100, partial(self._clear_pending, self._changeeventid))
        self._apply_state(state)

    def _apply_state(self, state):
        current_state = self.get_window_state()
        current_native_state = self.native.windowState()
        if (
            current_state == WindowState.MINIMIZED and not IS_WAYLAND
        ):  # pragma: no-cover-if-linux-wayland
            self.native.showNormal()
        if current_state == state:
            self._pending_state_transition = None
            return

        if current_state == WindowState.PRESENTATION:
            self.interface.screen = self._before_presentation_mode_screen
            self.native.menuBar().show()
            del self._before_presentation_mode_screen
            self._in_presentation_mode = False

        if state == WindowState.MAXIMIZED:
            self.native.showMaximized()

        # no-covered because MINIMIZED window state cannot be round-tripped
        # or asserted on Wayland.
        elif state == WindowState.MINIMIZED:  # pragma: no-cover-if-linux-wayland
            if not IS_WAYLAND:  # pragma: no branch
                self.native.showNormal()
            self.native.showMinimized()

        elif state == WindowState.FULLSCREEN:
            self.native.showFullScreen()
            if current_state == WindowState.PRESENTATION:
                # Fullscreen->Presentation doesn't register as a state change or
                # size change.
                QApplication.sendEvent(
                    self.native,
                    QWindowStateChangeEvent(current_native_state),
                )
                QApplication.sendEvent(
                    self.native, QResizeEvent(self.native.size(), self.native.size())
                )

        elif state == WindowState.PRESENTATION:
            self._before_presentation_mode_screen = self.interface.screen
            self.native.menuBar().hide()
            if self.toolbar_native:
                self.toolbar_native.hide()
            # Do this before showFullScreen because
            # showFullScreen might immediately trigger the event
            # and the window state read there might read a non-
            # presentation mode
            self._in_presentation_mode = True
            self.native.showFullScreen()
            if current_state == WindowState.FULLSCREEN:
                # Presentation->Fullscreen doesn't register as a state change or
                # size change.
                QApplication.sendEvent(
                    self.native, QWindowStateChangeEvent(current_native_state)
                )
                QApplication.sendEvent(
                    self.native, QResizeEvent(self.native.size(), self.native.size())
                )

        else:
            self.native.showNormal()

        QApplication.processEvents()

    def get_image_data(self):
        pixmap = self.container.native.grab()
        buffer = QBuffer()
        buffer.open(QIODevice.WriteOnly)
        pixmap.save(buffer, "PNG")
        img_bytes = bytes(buffer.data())
        buffer.close()
        return img_bytes

    def set_content(self, widget):
        self.container.content = widget


class MainWindow(Window):
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
        if self.interface.toolbar:
            if self.toolbar_native:
                self.toolbar_native.clear()
            else:
                self.toolbar_native = QToolBar(self.native)
                self.toolbar_native.setMovable(False)
                self.native.addToolBar(self.toolbar_native)
                self.toolbar_native.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

            prev_group = None

            for cmd in self.interface.toolbar:
                if isinstance(cmd, Separator):
                    self.toolbar_native.addSeparator()
                    prev_group = None
                    continue

                if prev_group is not None and prev_group != cmd.group:
                    self.toolbar_native.addSeparator()
                    prev_group = None
                else:
                    prev_group = cmd.group

                action = QAction(cmd.text, self.toolbar_native)

                if cmd.tooltip is not None:
                    action.setToolTip(cmd.tooltip)

                if cmd.icon is not None:
                    action.setIcon(cmd.icon._impl.native)

                action.setEnabled(cmd.enabled)

                action.triggered.connect(cmd.action)

                cmd._impl.native.append(action)

                self.toolbar_native.addAction(action)

        elif self.toolbar_native:
            self.native.removeToolBar(self.toolbar_native)
            self.toolbar_native.deleteLater()
            self.toolbar_native = None
