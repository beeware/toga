from pytest import skip

from toga_gtk.libs import Gtk


class SimpleProbe:
    def __init__(self, widget):
        self.widget = widget
        self.impl = widget._impl
        self.native = widget._impl.native
        assert isinstance(self.native, self.native_class)

    def assert_container(self, container):
        container_native = container._impl.container
        for control in container_native.get_children():
            if control == self.native:
                break
        else:
            raise ValueError(f"cannot find {self.native} in {container_native}")

    async def redraw(self):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Force a repaint
        while self.impl.container.needs_redraw or Gtk.events_pending():
            Gtk.main_iteration_do(blocking=False)

    @property
    def enabled(self):
        skip("enabled probe not implemented")

    @property
    def hidden(self):
        skip("hidden probe not implemented")

    @property
    def width(self):
        return self.native.get_allocation().width

    @property
    def height(self):
        return self.native.get_allocation().height
