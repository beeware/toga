from __future__ import annotations

from typing import TYPE_CHECKING

from toga.command import Separator
from toga.constants import WindowState
from toga.types import Position, Size
from toga.window import _initial_position

from .container import TogaContainer
from .libs import Gdk, Gtk
from .screens import Screen as ScreenImpl

if TYPE_CHECKING:  # pragma: no cover
    from toga.types import PositionT, SizeT


class Window:
    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.interface._impl = self

        self._is_closing = False

        self.layout = None

        self.create()
        self.native._impl = self

        self.native.connect("delete-event", self.gtk_delete_event)
        self.native.connect("window-state-event", self.gtk_window_state_event)

        self._window_state_flags = None

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

        self.native_toolbar = Gtk.Toolbar()
        self.native_toolbar.set_style(Gtk.ToolbarStyle.BOTH)
        self.native_toolbar.set_visible(False)
        self.toolbar_items = {}
        self.toolbar_separators = set()
        self.layout.pack_start(self.native_toolbar, expand=False, fill=False, padding=0)

        # Because expand and fill are True, the container will fill the available
        # space, and will get a size_allocate callback if the window is resized.
        self.container = TogaContainer()
        self.layout.pack_end(self.container, expand=True, fill=True, padding=0)

        self.native.add(self.layout)

    def create(self):
        self.native = Gtk.Window()

    ######################################################################
    # Native event handlers
    ######################################################################

    def gtk_window_state_event(self, widget, event):
        # Get the window state flags
        self._window_state_flags = event.new_window_state

    def gtk_delete_event(self, widget, data):
        if self._is_closing:
            should_close = True
        else:
            should_close = self.interface.on_close()

        # Return value of the GTK on_close handler indicates
        # whether the event has been fully handled. Returning
        # False indicates the event handling is *not* complete,
        # so further event processing (including actually
        # closing the window) should be performed.
        return not should_close

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
        if self.interface.content:
            self.interface.content.window = None
        self.interface.app.windows.discard(self.interface)

        self._is_closing = True
        self.native.close()

        self.interface._closed = True

    def create_toolbar(self):
        # If there's an existing toolbar, hide it until we know we need it.
        if self.toolbar_items:
            self.native_toolbar.set_visible(False)

        # Deregister any toolbar buttons from their commands, and remove them from the toolbar
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
            self.native_toolbar.set_visible(True)
            self.native_toolbar.show_all()

    def set_app(self, app):
        app.native.add_window(self.native)
        self.native.set_icon(app.interface.icon._impl.native(72))

    def show(self):
        self.native.show_all()

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
        size = self.native.get_size()
        return Size(size.width, size.height)

    def set_size(self, size: SizeT):
        self.native.resize(size[0], size[1])

    ######################################################################
    # Window position
    ######################################################################

    def get_current_screen(self):
        display = Gdk.Display.get_default()
        monitor_native = display.get_monitor_at_window(self.native.get_window())
        return ScreenImpl(monitor_native)

    def get_position(self) -> Position:
        pos = self.native.get_position()
        return Position(pos.root_x, pos.root_y)

    def set_position(self, position: PositionT):
        self.native.move(position[0], position[1])

    ######################################################################
    # Window visibility
    ######################################################################

    def get_visible(self):
        return self.native.get_property("visible")

    def hide(self):
        self.native.hide()

    ######################################################################
    # Window state
    ######################################################################

    def get_window_state(self):
        window_state_flags = self._window_state_flags
        if window_state_flags & Gdk.WindowState.MAXIMIZED:
            return WindowState.MAXIMIZED
        elif window_state_flags & Gdk.WindowState.ICONIFIED:
            return WindowState.MINIMIZED
        elif window_state_flags & Gdk.WindowState.FULLSCREEN:
            # Use a shadow variable since a window without any app menu and toolbar
            # in presentation mode would be indistinguishable from full screen mode.
            if getattr(self, "_is_in_presentation_mode", False) is True:
                return WindowState.PRESENTATION
            else:
                return WindowState.FULLSCREEN
        else:
            return WindowState.NORMAL

    def set_window_state(self, state):
        current_state = self.get_window_state()
        if state == WindowState.NORMAL:
            # If the window is maximized, restore it to its normal size
            if current_state == WindowState.MAXIMIZED:
                self.native.unmaximize()
            # Deminiaturize the window to restore it to its previous state
            elif current_state == WindowState.MINIMIZED:
                # deconify() doesn't work
                self.native.present()
            # If the window is in full-screen mode, exit full-screen mode
            elif current_state == WindowState.FULLSCREEN:
                self.native.unfullscreen()
            # If the window is in presentation mode, exit presentation mode
            elif current_state == WindowState.PRESENTATION:
                if isinstance(self.native, Gtk.ApplicationWindow):
                    self.native.set_show_menubar(True)
                # self.native_toolbar is always set to Gtk.Toolbar(), so no need
                # to check if self.native_toolbar exists.
                self.native_toolbar.set_visible(True)
                self.native.unfullscreen()

                self.interface.screen = self._before_presentation_mode_screen
                self._before_presentation_mode_screen = None
                self._is_in_presentation_mode = False
        else:
            if state == WindowState.MAXIMIZED:
                self.native.maximize()

            elif state == WindowState.MINIMIZED:
                self.native.iconify()

            elif state == WindowState.FULLSCREEN:
                self.native.fullscreen()

            elif state == WindowState.PRESENTATION:
                if getattr(self, "_before_presentation_mode_screen", None) is None:
                    self._before_presentation_mode_screen = self.interface.screen
                if isinstance(self.native, Gtk.ApplicationWindow):
                    self.native.set_show_menubar(False)
                # self.native_toolbar is always set to Gtk.Toolbar(), so no need
                # to check if self.native_toolbar exists.
                self.native_toolbar.set_visible(False)
                self.native.fullscreen()
                self._is_in_presentation_mode = True
            else:  # pragma: no cover
                # Marking this as no cover, since the type of the state parameter
                # value is checked on the interface.
                pass

    ######################################################################
    # Window capabilities
    ######################################################################

    def get_image_data(self):
        display = self.native.get_display()
        display.flush()

        # For some reason, converting the *window* to a pixbuf fails. But if you extract
        # a *part* of the overall screen, that works. So - work out the origin of the
        # window, then the allocation for the container relative to that window, and
        # capture that rectangle.
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
            # This shouldn't ever happen, and it's difficult to manufacture in test conditions
            raise ValueError(f"Unable to generate screenshot of {self}")
