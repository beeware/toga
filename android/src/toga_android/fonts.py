from pathlib import Path

from android import R
from android.graphics import Typeface
from android.util import TypedValue
from org.beeware.android import MainActivity

from toga.fonts import (
    _IMPL_CACHE,
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
    UnknownFontError,
)


class Font:
    def __init__(self, interface):
        self.interface = interface

    def load_predefined_system_font(self):
        """Use one of the system font names Toga predefines."""
        try:
            typeface = {
                # The default button font is not marked as bold, but it has a weight
                # of "medium" (500), which is in between "normal" (400), and "bold"
                # (600 or 700). To preserve this, we interpret SYSTEM as the widget's
                # original typeface.
                SYSTEM: None,
                MESSAGE: Typeface.DEFAULT,
                SERIF: Typeface.SERIF,
                SANS_SERIF: Typeface.SANS_SERIF,
                MONOSPACE: Typeface.MONOSPACE,
                # Android appears to not have a fantasy font available by default, but
                # if it ever does, we'll start using it. Android seems to choose a
                # serif font when asked for a fantasy font.
                FANTASY: Typeface.create("fantasy", Typeface.NORMAL),
                CURSIVE: Typeface.create("cursive", Typeface.NORMAL),
            }[self.interface.family]
        except KeyError as exc:
            msg = f"{self.interface} not a predefined system font"
            raise UnknownFontError(msg) from exc

        self._assign_native(typeface)

    def load_user_registered_font(self):
        """Use a font that the user has registered in their code."""
        font_key = self.interface._registered_font_key(
            self.interface.family,
            weight=self.interface.weight,
            style=self.interface.style,
            variant=self.interface.variant,
        )
        try:
            font_path = _REGISTERED_FONT_CACHE[font_key]
        except KeyError as exc:
            msg = f"{self.interface} not a user-registered font"
            raise UnknownFontError(msg) from exc

        # Yes, user has registered this font.
        if not Path(font_path).is_file():
            raise ValueError(f"Font file {font_path} could not be found")

        typeface = Typeface.createFromFile(font_path)
        if typeface is Typeface.DEFAULT:
            raise ValueError(f"Unable to load font file {font_path}")

        self._assign_native(typeface)

    def load_arbitrary_system_font(self):
        """Use a font available on the system."""
        raise UnknownFontError("Arbitrary system fonts not yet supported on Android")

    def _assign_native(self, typeface):
        style = 0
        if self.interface.weight == BOLD:
            style |= Typeface.BOLD
        if self.interface.style in {ITALIC, OBLIQUE}:
            style |= Typeface.ITALIC

        self.native_typeface = typeface
        self.native_style = style
        _IMPL_CACHE[self.interface] = self

    def typeface(self, *, default=Typeface.DEFAULT):
        """Return the appropriate native Typeface object."""
        typeface = default if self.native_typeface is None else self.native_typeface

        if self.native_style != typeface.getStyle():
            # While we're not caching this result, Android does its own caching of
            # different styles of the same Typeface.
            typeface = Typeface.create(typeface, self.native_style)

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
