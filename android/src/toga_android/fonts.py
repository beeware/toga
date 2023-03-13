import os

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

    def apply(self, tv, default_size):
        """Apply the font to the given native widget.

        :param tv: A native instance of TextView, or one of its subclasses.
        """
        if self.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
            tv.setTextSize(TypedValue.COMPLEX_UNIT_PX, default_size)
        else:
            # The default size for most widgets is 14sp, so mapping 1 Toga "point" to 1sp
            # will give relative sizes that are consistent with desktop platforms. It also
            # means font sizes will all change proportionately if the user adjusts the
            # text size in the system settings.
            tv.setTextSize(TypedValue.COMPLEX_UNIT_SP, self.interface.size)

        try:
            family = _FONT_CACHE[self.interface]
        except KeyError:
            family = None
            font_key = self.interface.registered_font_key(
                self.interface.family,
                weight=self.interface.weight,
                style=self.interface.style,
                variant=self.interface.variant,
            )
            if font_key in _REGISTERED_FONT_CACHE:
                font_path = str(
                    self.interface.factory.paths.app / _REGISTERED_FONT_CACHE[font_key]
                )
                if os.path.isfile(font_path):
                    family = Typeface.createFromFile(font_path)
                    # If the typeface cannot be created, following Exception is thrown:
                    # E/Minikin: addFont failed to create font, invalid request
                    # It does not kill the app, but there is currently no way to
                    # catch this Exception on Android
                else:
                    print(f"Registered font path {font_path!r} could not be found")

            if family is None:
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

            native_style = 0
            if self.interface.weight == BOLD:
                native_style = set_bits(native_style, Typeface.BOLD)
            if self.interface.style == ITALIC:
                native_style = set_bits(native_style, Typeface.ITALIC)
            family = Typeface.create(family, native_style)

            _FONT_CACHE[self.interface] = family

        tv.setTypeface(family)


def set_bits(input, mask, enable=True):
    if enable:
        output = input | mask
    else:
        output = input & ~mask
    return output
