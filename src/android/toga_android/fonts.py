import os

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
from toga.fonts import _REGISTERED_FONT_CACHE

from toga_android.libs.android.graphics import Typeface

_FONT_CACHE = {}


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
        elif self.interface.style == ITALIC:
            return Typeface.ITALIC
        else:
            return Typeface.NORMAL

    def get_typeface(self):
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
                font_path = str(self.interface.factory.paths.app / _REGISTERED_FONT_CACHE[font_key])
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

            family = family.__global__()  # store a JNI global reference to prevent objects from becoming stale
            _FONT_CACHE[self.interface] = family

        return family
