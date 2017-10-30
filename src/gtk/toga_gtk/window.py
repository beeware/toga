from gi.repository import Gtk

from toga.command import GROUP_BREAK, SECTION_BREAK
from toga.utils import wrapped_handler

from .container import Container
from . import dialogs


class Window:
    _IMPL_CLASS = Gtk.Window
    _CONTAINER_CLASS = Container
    _DIALOG_MODULE = dialogs

    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self.container = None
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
                item_impl.set_icon_widget(cmd._impl.icon._impl._impl_32)
                item_impl.set_label(cmd.label)
                item_impl.set_tooltip_text(cmd.tooltip)
                item_impl.connect("clicked", wrapped_handler(cmd, cmd.action))
                cmd._widgets.append(item_impl)
            self.toolbar_items[cmd] = item_impl
            self.toolbar_native.insert(item_impl, -1)

    def set_content(self, widget):
        if widget.native is None:
            self.container = Container()
            self.container.content = widget
        else:
            self.container = widget

        self._window_layout = Gtk.VBox()

        if self.toolbar_native:
            self._window_layout.pack_start(self.toolbar_native, False, False, 0)
        self._window_layout.pack_start(self.container.native, True, True, 0)

        self.native.add(self._window_layout)

        self.container.native.connect('size-allocate', self.on_size_allocate)

    def show(self):
        self.native.show_all()

    def on_close(self, widget, data):
        pass

    def on_size_allocate(self, widget, allocation):
        # print("ON WINDOW SIZE ALLOCATION", allocation.width, allocation.height)
        self.interface.content._update_layout(
            width=allocation.width,
            height=allocation.height
        )

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

