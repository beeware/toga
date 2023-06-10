from toga.command import GROUP_BREAK, SECTION_BREAK
from toga.handlers import wrapped_handler

from .container import TogaContainer
from .libs import Gtk


class Window:
    _IMPL_CLASS = Gtk.Window

    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.interface._impl = self

        self._is_closing = False

        self.layout = None

        self.native = self._IMPL_CLASS()
        self.native._impl = self

        self.native.connect("close-request", self.gtk_close_request)

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
        # Because vexpand and valign are set, the container will fill the
        # available space, and will get a size_allocate callback if the
        # window is resized.
        self.container = TogaContainer()
        self.container.set_valign(Gtk.Align.FILL)
        self.container.set_vexpand(True)
        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.layout.append(self.container)
        self.native.set_child(self.layout)

    def get_title(self):
        return self.native.get_title()

    def set_title(self, title):
        self.native.set_title(title)

    def set_app(self, app):
        app.native.add_window(self.native)

    def create_toolbar(self):
        # TODO: Implementing toolbar commands in HeaderBar; See #1931.
        self.interface.factory.not_implemented("Window.create_toolbar()")
        pass

    def clear_content(self):
        pass

    def set_content(self, widget):
        # Set the new widget to be the container's content
        self.container.content = widget

    def show(self):
        self.native.set_visible(True)

    def hide(self):
        self.native.set_visible(False)

    def get_visible(self):
        return self.native.get_property("visible")

    def gtk_close_request(self, data):
        if self._is_closing:
            should_close = True
        elif self.interface.on_close._raw:
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
        # Gtk believes/claims that positioning top level windows is not
        # the toolkit’s job but WM job. They are suggesting leaving
        # positioning to windowing system.
        # See https://discourse.gnome.org/t/how-to-center-gtkwindows-in-gtk4/3112/4
        self.interface.factory.not_implemented("Window.get_position()")
        pass

    def set_position(self, position):
        # Gtk believes/claims that positioning top level windows is not
        # the toolkit’s job but WM job. They are suggesting leaving
        # positioning to windowing system.
        # See https://discourse.gnome.org/t/how-to-center-gtkwindows-in-gtk4/3112/4
        self.interface.factory.not_implemented("Window.set_position()")
        pass

    def get_size(self):
        width = self.native.get_width()
        height = self.native.get_height()
        return width, height

    def set_size(self, size):
        self.native.set_default_size(size[0], size[1])

    def set_full_screen(self, is_full_screen):
        if is_full_screen:
            self.native.fullscreen()
        else:
            self.native.unfullscreen()
