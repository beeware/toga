from win32more.Microsoft.UI.Xaml.Controls import Grid, TextBlock

from .base import SimpleProbe
from .properties import brush_to_color, toga_x_text_align


class LabelProbe(SimpleProbe):
    native_class = Grid

    def __init__(self, widget):
        super().__init__(widget)
        self.label_native = self.impl.label_text.native
        assert isinstance(self.label_native, TextBlock)

    @property
    def text(self):
        return self.label_native.Text

    def assert_text_align(self, expected):
        assert expected == toga_x_text_align(self.label_native.TextAlignment)

    def assert_vertical_text_align(self, expected):
        # Vertical text alignment is not configurable for TextBlock.
        pass

    @property
    def color(self):
        return brush_to_color(self.label_native.Foreground)

    @property
    def enabled(self):
        # Neither TextBlock or Grid has the IsEnabled property.
        return True

    @property
    def font_family(self):
        return self.label_native.FontFamily

    @property
    def font_size(self):
        return self.label_native.FontSize

    @property
    def font_style(self):
        return self.label_native.FontStyle

    @property
    def font_weight(self):
        return self.label_native.FontWeight

    @property
    def native_cls(self):
        return type(self.label_native)
