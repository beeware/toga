from gi.repository import Gtk
from travertino.layout import Viewport

from toga.command import GROUP_BREAK, SECTION_BREAK
from toga.handlers import wrapped_handler

from . import dialogs


class GtkViewport:
    def __init__(self, native):
        self.native = native
        self.dpi = 96  # FIXME This is almost certainly wrong...

    @property
    def width(self):
        return self.native.get_allocated_width()

    @property
    def height(self):
        return self.native.get_allocated_height()


class Window:
    _IMPL_CLASS = Gtk.Window

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.create()

    def create(self):
        self.native = self._IMPL_CLASS()
        self.native.connect("delete-event", self.on_close)
        self.native.set_default_size(self.interface.size[0], self.interface.size[1])

        self.toolbar_native = None
        self.toolbar_items = None

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
                cmd._impl._widgets.remove(item_impl)

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
                cmd_impl = cmd.bind(self.interface.factory)
                icon_impl = cmd_impl.icon.bind(self.interface.factory)
                item_impl.set_icon_widget(icon_impl.native_32)
                item_impl.set_label(cmd.label)
                item_impl.set_tooltip_text(cmd.tooltip)
                item_impl.connect("clicked", wrapped_handler(cmd, cmd.action))
                cmd._widgets.append(item_impl)
            self.toolbar_items[cmd] = item_impl
            self.toolbar_native.insert(item_impl, -1)

    def set_content(self, widget):
        # Construct the top-level layout, and set the window's view to
        # the be the widget's native object.
        self.layout = Gtk.VBox()

        if self.toolbar_native:
            self.layout.pack_start(self.toolbar_native, False, False, 0)
        self.layout.pack_start(widget.native, True, True, 0)

        self.native.add(self.layout)

        # Make the window sensitive to size changes
        widget.native.connect('size-allocate', self.on_size_allocate)

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
        self.interface.content.style.layout(self.interface.content, Viewport(0, 0))
        self.interface.content._impl.min_width = self.interface.content.layout.width
        self.interface.content._impl.min_height = self.interface.content.layout.height

    def on_close(self, widget, data):
        pass

    def on_size_allocate(self, widget, allocation):
        # print("ON WINDOW SIZE ALLOCATION", allocation.width, allocation.height)
        pass

    def close(self):
        self.native.close()

    def set_position(self, position):
        pass

    def set_size(self, size):
        pass

    def info_dialog(self, title, message):
        return dialogs.info(self.interface, title, message)

    def question_dialog(self, title, message):
        return dialogs.question(self.interface, title, message)

    def confirm_dialog(self, title, message):
        return dialogs.confirm(self.interface, title, message)

    def error_dialog(self, title, message):
        return dialogs.error(self.interface, title, message)

    def stack_trace_dialog(self, title, message, content, retry=False):
        return dialogs.stack_trace(self.interface, title, message, content, retry)

    def save_file_dialog(self, title, suggested_filename, file_types):
        return dialogs.save_file(self.interface, title, suggested_filename, file_types)

