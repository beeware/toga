from pathlib import Path

from android import R
from android.graphics import Typeface
from android.util import TypedValue
from org.beeware.android import MainActivity

from toga.fonts import (
    _REGISTERED_FONT_CACHE,
    BOLD,
    CURSIVE,
    FANTASY,
    ITALIC,
    MESSAGE,
    MONOSPACE,
    OBLIQUE,
    SANS_SERIF,
    SERIF,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    SYSTEM_DEFAULT_FONTS,
)

_FONT_CACHE = {}


class Font:
    def __init__(self, interface):
        self.interface = interface

    def typeface(self, *, default=Typeface.DEFAULT):
        cache_key = (self.interface, default)
        if typeface := _FONT_CACHE.get(cache_key):
            return typeface

        font_key = self.interface._registered_font_key(
            self.interface.family,
            weight=self.interface.weight,
            style=self.interface.style,
            variant=self.interface.variant,
        )
        try:
            font_path = _REGISTERED_FONT_CACHE[font_key]
        except KeyError:
            # Not a pre-registered font
            if self.interface.family not in SYSTEM_DEFAULT_FONTS:
                print(
                    f"Unknown font '{self.interface}'; "
                    "using system font as a fallback"
                )
        else:
            if Path(font_path).is_file():
                typeface = Typeface.createFromFile(font_path)
                if typeface is Typeface.DEFAULT:
                    raise ValueError(f"Unable to load font file {font_path}")
            else:
                raise ValueError(f"Font file {font_path} could not be found")

        if typeface is None:
            if self.interface.family is SYSTEM:
                # The default button font is not marked as bold, but it has a weight
                # of "medium" (500), which is in between "normal" (400), and "bold"
                # (600 or 700). To preserve this, we use the widget's original
                # typeface as a starting point rather than Typeface.DEFAULT.
                typeface = default
            elif self.interface.family is MESSAGE:
                typeface = Typeface.DEFAULT
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
        if self.interface.weight == BOLD:
            native_style |= Typeface.BOLD
        if self.interface.style in {ITALIC, OBLIQUE}:
            native_style |= Typeface.ITALIC

        if native_style != typeface.getStyle():
            typeface = Typeface.create(typeface, native_style)

        _FONT_CACHE[cache_key] = typeface
        return typeface

    def size(self, *, default=None):
        """Return the font size in physical pixels."""
        context = MainActivity.singletonThis
        if self.interface.size == SYSTEM_DEFAULT_FONT_SIZE:
            if default is None:
                typed_array = context.obtainStyledAttributes(
                    R.style.TextAppearance_Small, [R.attr.textSize]
                )
                default = typed_array.getDimension(0, 0)
                typed_array.recycle()
            return default

        else:
            # Using SP means we follow the standard proportion between CSS pixels and
            # points by default, but respect the system text scaling setting.
            return TypedValue.applyDimension(
                TypedValue.COMPLEX_UNIT_SP,
                self.interface.size * (96 / 72),
                context.getResources().getDisplayMetrics(),
            )
