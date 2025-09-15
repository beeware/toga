from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

from toga.command import Separator
from toga.constants import WindowState
from toga.types import Position, Size
from toga.window import _initial_position

from .container import TogaContainer
from .libs import GTK_VERSION, IS_WAYLAND, Gdk, GLib, Gtk
from .screens import Screen as ScreenImpl

if TYPE_CHECKING:  # pragma: no cover
    from toga.types import PositionT, SizeT


class Window:
    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.interface._impl = self

        self.layout = None

        self.create()
        self.native._impl = self

        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self._delete_handler = self.native.connect(
                "delete-event",
                self.gtk_delete_event,
            )
        else:  # pragma: no-cover-if-gtk3
            self._delete_handler = self.native.connect(
                "close-request", self.gtk_delete_event
            )

        self.native.connect("show", self.gtk_show)
        self.native.connect("hide", self.gtk_hide)
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.connect("window-state-event", self.gtk_window_state_event)
            self.native.connect("focus-in-event", self.gtk_focus_in_event)
            self.native.connect("focus-out-event", self.gtk_focus_out_event)
        else:  # pragma: no-cover-if-gtk3
            self.native.connect("notify::fullscreened", self.gtk_window_state_event)
            self.native.connect("notify::maximized", self.gtk_window_state_event)
            self.native.connect("notify::minimized", self.gtk_window_state_event)

        self._window_state_flags = None
        self._in_presentation = False
        # Pending Window state transition variable:
        self._pending_state_transition = None

        self.native.set_default_size(size[0], size[1])

        self.set_title(title)
        self.set_position(position if position is not None else _initial_position())

        # Set the window deletable/closable.
        self.native.set_deletable(self.interface.closable)

        # Added to set Window Resizable - removes Window Maximize button from
        # Window Decorator when resizable == False
        self.native.set_resizable(self.interface.resizable)

        # The GTK window's content is the layout; any user content is placed
        # into the container, which is the bottom widget in the layout. The
        # toolbar (if required) will be added at the top of the layout.
        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Because expand and fill are True, the container will fill the available
        # space, and will get a size_allocate callback if the window is resized.
        self.container = TogaContainer()
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.layout.pack_end(self.container, expand=True, fill=True, padding=0)
            self.native.add(self.layout)
        else:  # pragma: no-cover-if-gtk3
            self.container.set_valign(Gtk.Align.FILL)
            self.container.set_vexpand(True)
            self.layout.append(self.container)
            self.native.set_child(self.layout)

    def create(self):
        self.native = Gtk.Window()

    ######################################################################
    # Native event handlers
    ######################################################################
    def gtk_show(self, widget):
        self.interface.on_show()

    def gtk_hide(self, widget):
        self.interface.on_hide()

    def gtk_window_state_event(self, widget, event):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            previous_window_state_flags = self._window_state_flags
            previous_state = self.get_window_state()
            # Get the window state flags
            self._window_state_flags = event.new_window_state
        else:  # pragma: no-cover-if-gtk3
            previous_window_state_flags = None
            previous_state = self.get_window_state()
            self._window_state_flags = None
        current_state = self.get_window_state()

        # Window state flags are unreliable when window is hidden,
        # so cache the previous window state flag on to the new
        # window state flag, so that get_window_state() would work
        # correctly.
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            if not self.get_visible():
                restore_flags = {
                    Gdk.WindowState.MAXIMIZED,
                    Gdk.WindowState.ICONIFIED,
                    Gdk.WindowState.FULLSCREEN,
                }
                for flag in restore_flags:
                    if previous_window_state_flags & flag:
                        self._window_state_flags |= flag
                        break
        else:  # pragma: no-cover-if-gtk3
            pass

        # Trigger the appropriate visibility events
        # Wayland doesn't allow for the detection of MINIMIZED, so the
        # visibility events will not be triggered when the window will
        # be minimized or un-minimized.
        if previous_state != current_state:
            if (
                previous_state == WindowState.MINIMIZED
            ):  # pragma: no-cover-if-linux-wayland
                self.interface.on_show()
            elif (
                current_state == WindowState.MINIMIZED
            ):  # pragma: no-cover-if-linux-wayland
                self.interface.on_hide()

        # Handle the pending state transitions
        if self._pending_state_transition:
            if current_state != WindowState.NORMAL:
                if self._pending_state_transition != current_state:
                    # Add a 10ms delay to wait for the native window state
                    # operation to complete to prevent glitching on wayland
                    # during rapid state switching.
                    #
                    # Ideally, we should use a native operation-completion
                    # callback event or a reliable native signal, but on
                    # testing none of the currently available gtk APIs or
                    # signals work reliably.
                    # For a list of native gtk APIs that were tested but didn't work:
                    # https://github.com/beeware/toga/pull/2473#discussion_r1833741222
                    #
                    if IS_WAYLAND:  # pragma: no-cover-if-linux-x
                        GLib.timeout_add(
                            10, partial(self._apply_state, WindowState.NORMAL)
                        )
                    else:  # pragma: no-cover-if-linux-wayland
                        self._apply_state(WindowState.NORMAL)
                else:
                    self._pending_state_transition = None
            else:
                if IS_WAYLAND:  # pragma: no-cover-if-linux-x
                    GLib.timeout_add(
                        10, partial(self._apply_state, self._pending_state_transition)
                    )
                else:  # pragma: no-cover-if-linux-wayland
                    self._apply_state(self._pending_state_transition)

    def gtk_delete_event(self, *_):
        # Return value of the GTK on_close handler indicates whether the event has been
        # fully handled. Returning True indicates the event has been handled, so further
        # handling (including actually closing the window) shouldn't be performed. This
        # handler must be deleted to allow the window to actually close.
        self.interface.on_close()
        return True

    def gtk_focus_in_event(self, sender, event):
        self.interface.on_gain_focus()

    def gtk_focus_out_event(self, sender, event):
        self.interface.on_lose_focus()

    ######################################################################
    # Window properties
    ######################################################################

    def get_title(self):
        return self.native.get_title()

    def set_title(self, title):
        self.native.set_title(title)

    ######################################################################
    # Window lifecycle
    ######################################################################

    def close(self):
        # Disconnect the delete handler so the close will complete
        self.native.disconnect(self._delete_handler)
        self.native.close()

    def set_app(self, app):
        app.native.add_window(self.native)
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.set_icon(app.interface.icon._impl.native(72))
        else:  # pragma: no-cover-if-gtk3
            self.interface.factory.not_implemented("Window.set_app() icon")

    def show(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.show_all()
        else:  # pragma: no-cover-if-gtk3
            self.native.present()

    ######################################################################
    # Window content and resources
    ######################################################################

    def set_content(self, widget):
        # Set the new widget to be the container's content
        self.container.content = widget

    ######################################################################
    # Window size
    ######################################################################

    def get_size(self) -> Size:
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            width, height = self.native.get_default_size()
            size = self.native.get_size()
            return Size(size.width, size.height)
        else:  # pragma: no-cover-if-gtk3
            width, height = self.native.get_default_size()
            return Size(width, height)

    def set_size(self, size: SizeT):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.resize(size[0], size[1])
        else:  # pragma: no-cover-if-gtk3
            self.native.set_default_size(size[0], size[1])

    ######################################################################
    # Window position
    ######################################################################

    def get_current_screen(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            display = Gdk.Display.get_default()
            monitor_native = display.get_monitor_at_window(self.native.get_window())
        else:  # pragma: no-cover-if-gtk3
            monitor_native = self.native.props.display
        return ScreenImpl(monitor_native)

    def get_position(self) -> Position:
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            pos = self.native.get_position()
            return Position(pos.root_x, pos.root_y)
        else:  # pragma: no-cover-if-gtk3
            # GTK4 no longer has an API to get position
            # since it isn't supported by Wayland
            return Position(0, 0)

    def set_position(self, position: PositionT):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.move(position[0], position[1])
        else:  # pragma: no-cover-if-gtk3
            # GTK4 no longer has an API to set position
            # since it isn't supported by Wayland
            pass

    ######################################################################
    # Window visibility
    ######################################################################

    def get_visible(self):
        return self.native.get_property("visible")

    def hide(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.hide()
        else:  # pragma: no-cover-if-gtk3
            self.native.set_visible(False)

    ######################################################################
    # Window state
    ######################################################################

    def get_window_state(self, in_progress_state=False):
        if in_progress_state and self._pending_state_transition:
            return self._pending_state_transition

        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            if not self._window_state_flags:
                return WindowState.NORMAL

            flags = self._window_state_flags
            if flags & Gdk.WindowState.MAXIMIZED:
                return WindowState.MAXIMIZED
            elif flags & Gdk.WindowState.ICONIFIED:
                return WindowState.MINIMIZED  # pragma: no-cover-if-linux-wayland
            elif flags & Gdk.WindowState.FULLSCREEN:
                return (
                    WindowState.PRESENTATION
                    if self._in_presentation
                    else WindowState.FULLSCREEN
                )

        else:  # pragma: no-cover-if-gtk3
            if self.native.is_maximized():
                return WindowState.MAXIMIZED
            elif GTK_VERSION >= (4, 12) and self.native.is_suspended():
                return WindowState.MINIMIZED
            elif self.native.is_fullscreen():
                return (
                    WindowState.PRESENTATION
                    if self._in_presentation
                    else WindowState.FULLSCREEN
                )

        return WindowState.NORMAL

    def set_window_state(self, state):
        if IS_WAYLAND and (
            state == WindowState.MINIMIZED
        ):  # pragma: no-cover-if-linux-x
            # Not implemented on wayland due to wayland interpretation of an app's
            # responsibility.
            return
        else:
            if self._pending_state_transition:
                self._pending_state_transition = state
            else:
                # If the app is in presentation mode, but this window isn't, then
                # exit app presentation mode before setting the requested state.
                if any(
                    window.state == WindowState.PRESENTATION
                    and window != self.interface
                    for window in self.interface.app.windows
                ):
                    self.interface.app.exit_presentation_mode()

                self._pending_state_transition = state
                if self.get_window_state() != WindowState.NORMAL:
                    self._apply_state(WindowState.NORMAL)
                else:
                    self._apply_state(state)

    def _apply_state(self, target_state):
        if target_state is None:  # pragma: no cover
            # This is OS delay related and is only sometimes triggered
            # when there is a delay in processing the states by the OS.
            # Hence, this branch cannot be consistently reached by the
            # testbed coverage.
            return

        current_state = self.get_window_state()
        if target_state == current_state:
            self._pending_state_transition = None
            return

        elif target_state == WindowState.MAXIMIZED:
            self.native.maximize()

        elif target_state == WindowState.MINIMIZED:  # pragma: no-cover-if-linux-wayland
            if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
                self.native.iconify()
            else:  # pragma: no-cover-if-gtk3
                self.native.minimize()

        elif target_state == WindowState.FULLSCREEN:
            self.native.fullscreen()

        elif target_state == WindowState.PRESENTATION:
            self._before_presentation_mode_screen = self.interface.screen
            if isinstance(self.native, Gtk.ApplicationWindow):
                self.native.set_show_menubar(False)
            if getattr(self, "native_toolbar", None):
                self.native_toolbar.set_visible(False)
            self.native.fullscreen()
            self._in_presentation = True

        else:  # target_state == WindowState.NORMAL:
            if current_state == WindowState.MAXIMIZED:
                self.native.unmaximize()

            elif (
                current_state == WindowState.MINIMIZED
            ):  # pragma: no-cover-if-linux-wayland
                # deiconify() doesn't work
                self.native.present()

            elif current_state == WindowState.FULLSCREEN:
                self.native.unfullscreen()

            else:  # current_state == WindowState.PRESENTATION:
                if isinstance(self.native, Gtk.ApplicationWindow):
                    self.native.set_show_menubar(True)
                if getattr(self, "native_toolbar", None):
                    self.native_toolbar.set_visible(True)
                self.native.unfullscreen()
                self.interface.screen = self._before_presentation_mode_screen
                del self._before_presentation_mode_screen
                self._in_presentation = False

    ######################################################################
    # Window capabilities
    ######################################################################

    def get_image_data(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            display = self.native.get_display()
            display.flush()

            # For some reason, converting the *window* to a pixbuf fails. But if you
            # extract a *part* of the overall screen, that works. So - work out the
            # origin of the window, then the allocation for the container relative to
            # that window, and capture that rectangle.
            window = self.native.get_window()
            origin = window.get_origin()
            allocation = self.container.get_allocation()

            screen = display.get_default_screen()
            root_window = screen.get_root_window()
            screenshot = Gdk.pixbuf_get_from_window(
                root_window,
                origin.x + allocation.x,
                origin.y + allocation.y,
                allocation.width,
                allocation.height,
            )

            success, buffer = screenshot.save_to_bufferv("png")
            if success:
                return buffer
            else:  # pragma: nocover
                # This shouldn't ever happen, and it's difficult to manufacture
                # in test conditions
                raise ValueError(f"Unable to generate screenshot of {self}")
        else:  # pragma: no-cover-if-gtk3
            self.interface.factory.not_implemented("Window.get_image_data()")


class MainWindow(Window):
    def create(self):
        self.native = Gtk.ApplicationWindow()
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            self.native.set_role("MainWindow")

            self.native_toolbar = Gtk.Toolbar()
            self.native_toolbar.set_style(Gtk.ToolbarStyle.BOTH)
            self.toolbar_items = {}
            self.toolbar_separators = set()
        else:  # pragma: no-cover-if-gtk3
            pass

    def create_menus(self):
        # GTK menus are handled at the app level
        pass

    def create_toolbar(self):
        if GTK_VERSION < (4, 0, 0):  # pragma: no-cover-if-gtk4
            # If there's an existing toolbar, hide it until we know we need it.
            self.layout.remove(self.native_toolbar)

            # Deregister any toolbar buttons from their commands, and remove them
            # from the toolbar
            for cmd, item_impl in self.toolbar_items.items():
                self.native_toolbar.remove(item_impl)
                cmd._impl.native.remove(item_impl)

            # Remove any toolbar separators
            for sep in self.toolbar_separators:
                self.native_toolbar.remove(sep)

            # Create the new toolbar items
            self.toolbar_items = {}
            self.toolbar_separators = set()
            prev_group = None
            for cmd in self.interface.toolbar:
                if isinstance(cmd, Separator):
                    item_impl = Gtk.SeparatorToolItem()
                    item_impl.set_draw(False)
                    self.toolbar_separators.add(item_impl)
                    prev_group = None
                else:
                    # A change in group requires adding a toolbar separator
                    if prev_group is not None and prev_group != cmd.group:
                        group_sep = Gtk.SeparatorToolItem()
                        group_sep.set_draw(True)
                        self.toolbar_separators.add(group_sep)
                        self.native_toolbar.insert(group_sep, -1)
                        prev_group = None
                    else:
                        prev_group = cmd.group

                    item_impl = Gtk.ToolButton()
                    if cmd.icon:
                        item_impl.set_icon_widget(
                            Gtk.Image.new_from_pixbuf(cmd.icon._impl.native(32))
                        )
                    item_impl.set_label(cmd.text)
                    if cmd.tooltip:
                        item_impl.set_tooltip_text(cmd.tooltip)
                    item_impl.connect("clicked", cmd._impl.gtk_clicked)
                    cmd._impl.native.append(item_impl)
                    self.toolbar_items[cmd] = item_impl

                self.native_toolbar.insert(item_impl, -1)

            if self.toolbar_items:
                # We have toolbar items; add the toolbar to the top of the layout.
                self.layout.pack_start(
                    self.native_toolbar,
                    expand=False,
                    fill=False,
                    padding=0,
                )
                self.native_toolbar.show_all()
        else:  # pragma: no-cover-if-gtk3
            # TODO: Implement toolbar commands in HeaderBar with #1931
            pass
