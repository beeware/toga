from toga.command import GROUP_BREAK, SECTION_BREAK
from toga.handlers import wrapped_handler
from toga.window import WindowState

from .container import TogaContainer
from .libs import Gdk, Gtk


class Window:
    _IMPL_CLASS = Gtk.Window

    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.interface._impl = self

        self._is_closing = False

        self.layout = None

        self.native = self._IMPL_CLASS()
        self.native._impl = self

        self.native.connect("delete-event", self.gtk_delete_event)

        self.native.set_default_size(size[0], size[1])

        self.set_title(title)
        self.set_position(position)

        # Set the window deletable/closeable.
        self.native.set_deletable(self.interface.closeable)

        # Added to set Window Resizable - removes Window Maximize button from
        # Window Decorator when resizable == False
        self.native.set_resizable(self.interface.resizeable)

        self.toolbar_native = None
        self.toolbar_items = None

        # The GTK window's content is the layout; any user content is placed
        # into the container, which is the bottom widget in the layout. The
        # toolbar (if required) will be added at the top of the layout.
        #
        # Because expand and fill are True, the container will fill the available
        # space, and will get a size_allocate callback if the window is resized.
        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.container = TogaContainer()
        self.layout.pack_end(self.container, expand=True, fill=True, padding=0)
        self.native.add(self.layout)

        self._window_state = WindowState.NORMAL
        # Connect the "window-state-event" signal to the on_window_state_event() function
        self.native.connect("window-state-event", self.on_window_state_event)

    def on_window_state_event(self, widget, event):
        # Get the window state
        instantaneous_state = event.new_window_state

        if instantaneous_state & Gdk.WindowState.MAXIMIZED:
            self._window_state = WindowState.MAXIMIZED
        elif instantaneous_state & Gdk.WindowState.ICONIFIED:
            self._window_state = WindowState.MINIMIZED
        elif instantaneous_state & Gdk.WindowState.FULLSCREEN:
            self._window_state = WindowState.FULLSCREEN
        else:
            self._window_state = WindowState.NORMAL

    def get_title(self):
        return self.native.get_title()

    def set_title(self, title):
        self.native.set_title(title)

    def set_app(self, app):
        app.native.add_window(self.native)

    def create_toolbar(self):
        if self.toolbar_items is None:
            self.toolbar_native = Gtk.Toolbar()
            self.toolbar_items = {}
            self.layout.pack_start(
                self.toolbar_native, expand=False, fill=False, padding=0
            )
        else:
            for cmd, item_impl in self.toolbar_items.items():
                self.toolbar_native.remove(item_impl)
                cmd._impl.native.remove(item_impl)

        self.toolbar_native.set_style(Gtk.ToolbarStyle.BOTH)
        for cmd in self.interface.toolbar:
            if cmd == GROUP_BREAK:
                item_impl = Gtk.SeparatorToolItem()
                item_impl.set_draw(True)
            elif cmd == SECTION_BREAK:
                item_impl = Gtk.SeparatorToolItem()
                item_impl.set_draw(False)
            else:
                item_impl = Gtk.ToolButton()
                if cmd.icon:
                    item_impl.set_icon_widget(cmd.icon._impl.native_32)
                item_impl.set_label(cmd.text)
                item_impl.set_tooltip_text(cmd.tooltip)
                item_impl.connect("clicked", wrapped_handler(cmd, cmd.action))
                cmd._impl.native.append(item_impl)
            self.toolbar_items[cmd] = item_impl
            self.toolbar_native.insert(item_impl, -1)

    def clear_content(self):
        pass

    def set_content(self, widget):
        # Set the new widget to be the container's content
        self.container.content = widget

    def show(self):
        self.native.show_all()

    def hide(self):
        self.native.hide()

    def get_visible(self):
        return self.native.get_property("visible")

    def gtk_delete_event(self, widget, data):
        if self._is_closing:
            should_close = True
        elif self.interface.on_close:
            should_close = self.interface.on_close(self.interface.app)
        else:
            should_close = True

        # Return value of the GTK on_close handler indicates
        # whether the event has been fully handled. Returning
        # False indicates the event handling is *not* complete,
        # so further event processing (including actually
        # closing the window) should be performed.
        return not should_close

    def close(self):
        self._is_closing = True
        self.native.close()

    def get_position(self):
        pos = self.native.get_position()
        return pos.root_x, pos.root_y

    def set_position(self, position):
        self.native.move(position[0], position[1])

    def get_size(self):
        size = self.native.get_size()
        return size.width, size.height

    def set_size(self, size):
        self.native.resize(size[0], size[1])

    def get_window_state(self):
        return self._window_state

    def set_window_state(self, state, screen=None):
        if screen is not None:
            screen_native = screen.native
        else:
            screen_native = self.native.get_screen()

        display = screen_native.get_display()
        window = self.native.get_window()
        monitor = Gdk.Display.get_monitor_at_window(display, window)
        geometry = Gdk.Monitor.get_geometry(monitor)

        if state == WindowState.NORMAL:
            current_state = self.get_window_state()
            if current_state == WindowState.MAXIMIZED:
                self.native.unmaximize()
            elif current_state == WindowState.MINIMIZED:
                self.native.deiconify()
            elif current_state == WindowState.FULLSCREEN:
                self.native.unfullscreen()
            self._window_state = WindowState.NORMAL

        elif state == WindowState.MAXIMIZED:
            self.native.move(geometry.x, geometry.y)
            self.native.set_size_request(geometry.width, geometry.height)
            self.native.maximize()
            self._window_state = WindowState.MAXIMIZED

        elif state == WindowState.MINIMIZED:
            self.native.move(geometry.x, geometry.y)
            self.native.set_size_request(geometry.width, geometry.height)
            self.native.iconify()
            self._window_state = WindowState.MINIMIZED

        elif state == WindowState.FULLSCREEN:
            self.native.move(geometry.x, geometry.y)
            self.native.set_size_request(geometry.width, geometry.height)
            self.native.fullscreen()
            self._window_state = WindowState.FULLSCREEN

        else:
            return

    def set_full_screen(self, is_full_screen):
        if is_full_screen:
            self.native.fullscreen()
        else:
            self.native.unfullscreen()
