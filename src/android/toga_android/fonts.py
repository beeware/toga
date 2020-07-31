from toga.fonts import (
    BOLD,
    CURSIVE,
    FANTASY,
    ITALIC,
    MONOSPACE,
    SANS_SERIF,
    SERIF,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
)

from .libs.android_widgets import (
    Typeface,
)


class Font:
    def __init__(self, interface):
        self.interface = interface

    def get_size(self):
        # Default system font size on Android is 14sp (sp = dp, but is separately
        # scalable in user settings). For what it's worth, Toga's default is 12pt.
        if self.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
            font_size = 14
        else:
            font_size = self.interface.size
        return float(font_size)

    def get_style(self):
        if self.interface.weight == BOLD:
            if self.interface.style == ITALIC:
                return Typeface.BOLD_ITALIC
            else:
                return Typeface.BOLD
        if self.interface.style == ITALIC:
            return Typeface.ITALIC
        return Typeface.NORMAL

    def get_typeface(self):
        if self.interface.family is SYSTEM:
            family = Typeface.DEFAULT
        elif self.interface.family is SERIF:
            family = Typeface.SERIF
        elif self.interface.family is SANS_SERIF:
            family = Typeface.SANS_SERIF
        elif self.interface.family is MONOSPACE:
            family = Typeface.MONOSPACE
        elif self.interface.family is CURSIVE:
            family = Typeface.create("cursive", Typeface.NORMAL)
        elif self.interface.family is FANTASY:
            # Android appears to not have a fantasy font available by default,
            # but if it ever does, we'll start using it. Android seems to choose
            # a serif font when asked for a fantasy font.
            family = Typeface.create("fantasy", Typeface.NORMAL)
        else:
            family = Typeface.create(self.interface.family, Typeface.NORMAL)

        return family
