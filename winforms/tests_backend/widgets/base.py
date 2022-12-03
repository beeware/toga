from System import EventArgs, Object

from .properties import toga_color


class SimpleProbe:
    def __init__(self, widget, container):
        for control in container._impl.native.Controls:
            if Object.ReferenceEquals(control, widget._impl.native):
                self.native = control
                assert isinstance(self.native, self.native_class)
                break
        else:
            raise ValueError(f"cannot find {widget} in {container}")

    @property
    def enabled(self):
        return self.native.Enabled

    @property
    def background_color(self):
        return toga_color(self.native.BackColor)

    @property
    def color(self):
        return toga_color(self.native.ForeColor)

    @property
    def hidden(self):
        return not self.native.Visible

    @property
    def width(self):
        return self.native.Width

    @property
    def height(self):
        return self.native.Height

    def press(self):
        self.native.OnClick(EventArgs.Empty)
