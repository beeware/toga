import os

import toga
from toga.fonts import (
    _REGISTERED_FONT_CACHE,
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
from toga_android.libs.android.graphics import Typeface
from toga_android.libs.android.util import TypedValue

_FONT_CACHE = {}


class Font:
    def __init__(self, interface):
        self.interface = interface

    def apply(self, tv, default_size, default_typeface):
        """Apply the font to the given native widget.

        :param tv: A native instance of TextView, or one of its subclasses.
        :param default_size: The default font size of this widget, in pixels.
        :param default_typeface: The default Typeface of this widget.
        """
        if self.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
            tv.setTextSize(TypedValue.COMPLEX_UNIT_PX, default_size)
        else:
            # The default size for most widgets is 14sp, so mapping 1 Toga "point" to 1sp
            # will give relative sizes that are consistent with desktop platforms. Using
            # SP means font sizes will all change proportionately if the user adjusts the
            # text size in the system settings.
            tv.setTextSize(TypedValue.COMPLEX_UNIT_SP, self.interface.size)

        cache_key = (self.interface, default_typeface)
        try:
            typeface = _FONT_CACHE[cache_key]
        except KeyError:
            typeface = None
            font_key = self.interface.registered_font_key(
                self.interface.family,
                weight=self.interface.weight,
                style=self.interface.style,
                variant=self.interface.variant,
            )
            if font_key in _REGISTERED_FONT_CACHE:
                font_path = str(
                    toga.App.app.paths.app / _REGISTERED_FONT_CACHE[font_key]
                )
                if os.path.isfile(font_path):
                    typeface = Typeface.createFromFile(font_path)
                    # If the typeface cannot be created, following Exception is thrown:
                    # E/Minikin: addFont failed to create font, invalid request
                    # It does not kill the app, but there is currently no way to
                    # catch this Exception on Android
                else:
                    print(f"Registered font path {font_path!r} could not be found")

            if typeface is None:
                if self.interface.family is SYSTEM:
                    # The default button font is not marked as bold, but it has a weight
                    # of "medium" (500), which is in between "normal" (400), and "bold"
                    # (600 or 700). To preserve this, we use the widget's original
                    # typeface as a starting point rather than Typeface.DEFAULT.
                    typeface = default_typeface
                elif self.interface.family is SERIF:
                    typeface = Typeface.SERIF
                elif self.interface.family is SANS_SERIF:
                    typeface = Typeface.SANS_SERIF
                elif self.interface.family is MONOSPACE:
                    typeface = Typeface.MONOSPACE
                elif self.interface.family is CURSIVE:
                    typeface = Typeface.create("cursive", Typeface.NORMAL)
                elif self.interface.family is FANTASY:
                    # Android appears to not have a fantasy font available by default,
                    # but if it ever does, we'll start using it. Android seems to choose
                    # a serif font when asked for a fantasy font.
                    typeface = Typeface.create("fantasy", Typeface.NORMAL)
                else:
                    typeface = Typeface.create(self.interface.family, Typeface.NORMAL)

            native_style = typeface.getStyle()
            if self.interface.weight is not None:
                native_style = set_bits(
                    native_style, Typeface.BOLD, self.interface.weight == BOLD
                )
            if self.interface.style is not None:
                native_style = set_bits(
                    native_style, Typeface.ITALIC, self.interface.style == ITALIC
                )
            if native_style != typeface.getStyle():
                typeface = Typeface.create(typeface, native_style)

            _FONT_CACHE[cache_key] = typeface

        tv.setTypeface(typeface)


def set_bits(input, mask, enable=True):
    if enable:
        output = input | mask
    else:
        output = input & ~mask
    return output
