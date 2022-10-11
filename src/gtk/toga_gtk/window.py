from toga.command import GROUP_BREAK, SECTION_BREAK
from toga.handlers import wrapped_handler

from .libs import Gtk


class GtkViewport:
    def __init__(self, native):
        self.native = native
        # GDK/GTK always renders at 96dpi. When HiDPI mode is enabled, it is
        # managed at the compositor level. See
        # https://wiki.archlinux.org/index.php/HiDPI#GDK_3_(GTK_3) for details
        self.dpi = 96
        self.baseline_dpi = self.dpi

    @property
    def width(self):
        # Treat `native=None` as a 0x0 viewport.
        if self.native is None:
            return 0
        return self.native.get_allocated_width()

    @property
    def height(self):
        if self.native is None:
            return 0
        return self.native.get_allocated_height()


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
                    icon_impl = cmd.icon.bind(self.interface.factory)
                    item_impl.set_icon_widget(icon_impl.native_32)
                item_impl.set_label(cmd.text)
                item_impl.set_tooltip_text(cmd.tooltip)
                item_impl.connect("clicked", wrapped_handler(cmd, cmd.action))
                cmd._impl.native.append(item_impl)
            self.toolbar_items[cmd] = item_impl
            self.toolbar_native.insert(item_impl, -1)

    def clear_content(self):
        if self.interface.content:
            for child in self.interface.content.children:
                child._impl.container = None

    def set_content(self, widget):
        # Construct the top-level layout, and set the window's view to
        # the be the widget's native object.
        # Alaway avoid using deprecated widgets and methods.
        if self.layout:
            self.native.remove(self.layout)

        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        if self.toolbar_native:
            self.layout.pack_start(self.toolbar_native, False, False, 0)
        self.layout.pack_start(widget.native, True, True, 0)

        self.native.add(self.layout)

        # Make the window sensitive to size changes
        widget.native.connect('size-allocate', self.gtk_size_allocate)

        # Set the widget's viewport to be based on the window's content.
        widget.viewport = GtkViewport(widget.native)

        # Add all children to the content widget.
        for child in widget.interface.children:
            child._impl.container = widget

    def show(self):
        self.native.show_all()

        # Now that the content is visible, we can do our initial hinting,
        # and use that as the basis for setting the minimum window size.
        self.interface.content._impl.rehint()
        self.interface.content.style.layout(
            self.interface.content,
            GtkViewport(native=None)
        )
        self.interface.content._impl.min_width = self.interface.content.layout.width
        self.interface.content._impl.min_height = self.interface.content.layout.height

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

    def set_on_close(self, handler):
        pass

    def gtk_size_allocate(self, widget, allocation):
        #  ("ON WINDOW SIZE ALLOCATION", allocation.width, allocation.height)
        pass

    def close(self):
        self._is_closing = True
        self.native.close()

    def get_position(self):
        pos = self.native.get_position()
        return (pos.root_x, pos.root_y)

    def set_position(self, position):
        self.native.move(position[0], position[1])

    def get_size(self):
        size = self.native.get_size()
        return (size.width, size.height)

    def set_size(self, size):
        self.native.resize(size[0], size[1])

    def set_full_screen(self, is_full_screen):
        if is_full_screen:
            self.native.fullscreen()
        else:
            self.native.unfullscreen()
