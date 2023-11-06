from toga.command import GROUP_BREAK, SECTION_BREAK

from .container import TogaContainer
from .libs import Gdk, Gtk


def gtk_toolbar_item_clicked(cmd):
    """Convert a GTK toolbar item click into a command invocation."""

    def _handler(widget):
        cmd.action()

    return _handler


class Window:
    def __init__(self, interface, title, position, size):
        self.interface = interface
        self.interface._impl = self

        self._is_closing = False

        self.layout = None

        self.create()
        self.native._impl = self

        self.native.connect("close-request", self.gtk_close_request)

        self.native.set_default_size(size[0], size[1])

        self.set_title(title)
        self.set_position(position)

        # Set the window deletable/closable.
        self.native.set_deletable(self.interface.closable)

        # Added to set Window Resizable - removes Window Maximize button from
        # Window Decorator when resizable == False
        self.native.set_resizable(self.interface.resizable)

        # The GTK window's content is the layout; any user content is placed
        # into the container, which is the bottom widget in the layout. The
        # toolbar (if required) will be added at the top of the layout.

        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.layout.append(self.container)

        # Because vexpand and valign are set, the container will fill the
        # available space, and will get a size_allocate callback if the
        # window is resized.
        self.container = TogaContainer()
        self.container.set_valign(Gtk.Align.FILL)
        self.container.set_vexpand(True)

        self.native.set_child(self.layout)

    def create(self):
        self.native = Gtk.Window()

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
        else:
            should_close = self.interface.on_close()

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
