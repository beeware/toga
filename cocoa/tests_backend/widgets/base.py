# from System import EventArgs, Object

from .properties import toga_color


class SimpleProbe:
    def __init__(self, widget):
        self.native = widget._impl.native
        assert isinstance(self.native, self.native_class)

    def assert_container(self, container):
        container_native = container._impl.native
        for control in container_native.subviews:
            if control == self.native:
                break
        else:
            raise ValueError(f"cannot find {self.native} in {container_native}")

    @property
    def enabled(self):
        return self.native.enabled

    @property
    def background_color(self):
        return toga_color(self.native.backgroundColor)

    @property
    def color(self):
        return toga_color(self.native.textColor)

    @property
    def hidden(self):
        return self.native.hidden

    @property
    def width(self):
        return self.native.frame.width

    @property
    def height(self):
        return self.native.frame.height

    def press(self):
        self.native.performClick(None)
