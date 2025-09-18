import pytest

from ..fonts import FontMixin
from ..probe import BaseProbe


class SimpleProbe(BaseProbe, FontMixin):
    def __init__(self, widget):
        super().__init__()
        self.app = widget.app
        self.window = widget.window
        self.widget = widget
        self.impl = widget._impl
        self.native = widget._impl.native
        assert isinstance(self.native, self.native_class)

    def assert_container(self, container):
        assert container._impl.container == self.impl.container
        container_native = container._impl.container.native
        for obj in container_native.children():
            if obj == self.native:
                break
        else:
            raise ValueError(f"cannot find {self.native} in {container_native}")

    def assert_not_contained(self):
        assert self.widget._impl.container is None
        assert self.native.parentWidget() is None

    def assert_text_align(self, expected):
        pytest.xfail("fonts not impld on qt")

    @property
    def enabled(self):
        return self.native.isEnabled()

    @property
    def color(self):
        pytest.skip("Colors not implemented on Qt")

    @property
    def background_color(self):
        pytest.skip("Colors not implemented on Qt")

    @property
    def hidden(self):
        return not self.native.isVisible()

    @property
    def shrink_on_resize(self):
        return True

    def assert_layout(self, size, position):
        # Widget is contained and in a window.
        assert self.widget._impl.container is not None
        assert self.native.parentWidget() is not None

        assert (self.native.width(), self.native.height()) == size
        assert (self.native.pos().x(), self.native.pos().y()) == position

    async def press(self):
        self.native.click()

    def mouse_event(self, x=0, y=0, **kwargs):
        pytest.fail("Please implement the mouse event probe")

    @property
    def is_hidden(self):
        return not self.native.isVisible()

    @property
    def has_focus(self):
        return self.native.hasFocus()

    @property
    def width(self):
        return self.native.width()

    def assert_width(self, min_width, max_width):
        assert min_width <= self.width <= max_width

    def assert_height(self, min_height, max_height):
        assert min_height <= self.height <= max_height

    @property
    def height(self):
        return self.native.height()

    async def undo(self):
        pytest.skip("Undo not supported by default on widgets")

    async def redo(self):
        pytest.skip("Redo not supported by default on widgets")
