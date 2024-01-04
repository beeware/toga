from .container import TogaContainer
from .libs import Gtk


class TogaWindow(Gtk.Window):
    def do_snapshot(self, snapshot):
        self.snapshot = snapshot
        Gtk.ApplicationWindow.do_snapshot(self, self.snapshot)


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

        # Because vexpand and valign are set, the container will fill the
        # available space, and will get a size_allocate callback if the
        # window is resized.
        self.container = TogaContainer()
        self.container.set_valign(Gtk.Align.FILL)
        self.container.set_vexpand(True)
        self.layout.append(self.container)

        self.native.set_child(self.layout)

    def create(self):
        self.native = TogaWindow()

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
        child = self.native.get_last_child()
        while child is not None:
            child.set_visible(True)
            child = child.get_prev_sibling()

    def hide(self):
        self.native.set_visible(False)

    def get_visible(self):
        return self.native.get_visible()

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
        pass

    def set_position(self, position):
        # Does nothing on gtk4
        pass

    def get_size(self):
        width, height = self.native.get_default_size()
        return width, height

    def set_size(self, size):
        self.native.set_default_size(size[0], size[1])

    def set_full_screen(self, is_full_screen):
        if is_full_screen:
            self.native.fullscreen()
        else:
            self.native.unfullscreen()

    def get_image_data(self):
        # FIXME: The following should be work but it doesn't. Please, see this
        # https://gitlab.gnome.org/GNOME/pygobject/-/issues/601 for details.
        # snapshot_node = self.native.snapshot.to_node()
        # screenshot_texture = self.native.get_renderer().render_texture(
        #     snapshot_node, None
        # )
        # screenshot = screenshot_texture.save_to_png_bytes()
        # return screenshot.get_data()
        self.interface.factory.not_implemented("Window.get_image_data()")
        pass
