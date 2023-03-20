from java import jclass

from android.graphics.drawable import DrawableWrapper, LayerDrawable
from toga.fonts import SYSTEM

from .label import LabelProbe
from .properties import toga_color


# On Android, a Button is just a TextView with a state-dependent background image.
class ButtonProbe(LabelProbe):
    native_class = jclass("android.widget.Button")

    def assert_font_family(self, expected):
        actual = self.font.family
        if expected == SYSTEM:
            assert actual == "sans-serif-medium"
        else:
            assert actual == expected

    @property
    def background_color(self):
        background = self.native.getBackground()
        while True:
            if isinstance(background, LayerDrawable):
                # LayerDrawable applies color filters to all of its layers, but it doesn't
                # implement getColorFilter itself.
                background = background.getDrawable(0)
            elif isinstance(background, DrawableWrapper):
                # DrawableWrapper doesn't implement getColorFilter in API level 24, but
                # has implemented it by API level 33.
                background = background.getDrawable()
            else:
                break

        filter = background.getColorFilter()
        if filter:
            # PorterDuffColorFilter.getColor is undocumented, but continues to work for
            # now. If this method is blocked in the future, another option is to use the
            # filter to draw something and see what color comes out.
            return toga_color(filter.getColor())
        else:
            return None
