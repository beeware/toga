from gi.repository import Gtk

from toga.command import GROUP_BREAK, SECTION_BREAK

from .container import Container
from .utils import wrapped_handler
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

        self._toolbar_impl = None
        self._toolbar_items = None

    def set_title(self, title):
        self.native.set_title(title)

    def set_app(self, app):
        # app.native.add_window(self.native)
        pass

    def create_toolbar(self):
        if self._toolbar_items is None:
            self._toolbar_impl = Gtk.Toolbar()
            self._toolbar_items = {}
        else:
            for cmd, item_impl in self._toolbar_items.items():
                self._toolbar_impl.remove(item_impl)
                cmd._widgets.remove(item_impl)

        self._toolbar_impl.set_style(Gtk.ToolbarStyle.BOTH)
        for cmd in self.interface.toolbar:
            if cmd == GROUP_BREAK:
                item_impl = Gtk.SeparatorToolItem()
                item_impl.set_draw(True)
            elif cmd == SECTION_BREAK:
                item_impl = Gtk.SeparatorToolItem()
                item_impl.set_draw(False)
            else:
                item_impl = Gtk.ToolButton()
                item_impl.set_icon_widget(cmd.icon._impl_32)
                item_impl.set_label(cmd.label)
                item_impl.set_tooltip_text(cmd.tooltip)
                item_impl.connect("clicked", wrapped_handler(cmd, cmd.action))
                cmd._widgets.append(item_impl)
            self._toolbar_items[cmd] = item_impl
            self._toolbar_impl.insert(item_impl, -1)

    def set_content(self, widget):
        print('window._impl.set_content')
        if widget.native is None:
            self.container = Container()
            self.container.content = widget
        else:
            self.container = widget

        self._window_layout = Gtk.VBox()

        if self._toolbar_impl:
            self._window_layout.pack_start(self._toolbar_impl, False, False, 0)
        self._window_layout.pack_start(self.container.native, True, True, 0)

        self.native.add(self._window_layout)

        self.container.native.connect('size-allocate', self.on_size_allocate)

    def show(self):
        print('window._impl.show')
        self.native.show_all()

    def on_close(self, widget, data):
        print('window._impl.close')
        self.on_close()

    def on_size_allocate(self, widget, allocation):
        print("ON WINDOW SIZE ALLOCATION", allocation.width, allocation.height)
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
