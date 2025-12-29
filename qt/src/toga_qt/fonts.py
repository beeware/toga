from pathlib import Path

from PySide6.QtGui import QFont, QFontDatabase

from toga.fonts import (
    _IMPL_CACHE,
    _REGISTERED_FONT_CACHE,
    BOLD,
    CURSIVE,
    FANTASY,
    ITALIC,
    MESSAGE,
    MONOSPACE,
    NORMAL,
    OBLIQUE,
    SANS_SERIF,
    SERIF,
    SMALL_CAPS,
    SYSTEM,
    SYSTEM_DEFAULT_FONT_SIZE,
    SYSTEM_DEFAULT_FONTS,
    UnknownFontError,
)

QT_FONT_STYLE_HINTS = {
    SYSTEM: QFont.StyleHint.System,
    MESSAGE: QFont.StyleHint.System,
    CURSIVE: QFont.StyleHint.Cursive,
    FANTASY: QFont.StyleHint.Fantasy,
    MONOSPACE: QFont.StyleHint.Monospace,
    SANS_SERIF: QFont.StyleHint.SansSerif,
    SERIF: QFont.StyleHint.Serif,
}
QT_FONT_STYLES = {
    NORMAL: QFont.Style.StyleNormal,
    ITALIC: QFont.Style.StyleItalic,
    OBLIQUE: QFont.Style.StyleOblique,
}
QT_FONT_WEIGHTS = {
    NORMAL: QFont.Weight.Normal,
    BOLD: QFont.Weight.Bold,
}

# Names of user-registered fonts loaded into QFontDatabase
_CUSTOM_FONT_NAMES = {}


class Font:
    def __init__(self, interface):
        self.interface = interface

    def load_predefined_system_font(self):
        """Use one of the system font names Toga predefines."""
        if self.interface.family not in SYSTEM_DEFAULT_FONTS:
            raise UnknownFontError(f"{self.interface} not a predefined system font")

        if self.interface.family in {SYSTEM, MESSAGE}:
            font = QFontDatabase.systemFont(QFontDatabase.SystemFont.GeneralFont)
        elif self.interface.family == MONOSPACE:
            font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        else:
            font = QFont()
            # Qt recognises standard predefined font names.
            font.setFamily(self.interface.family)
            font.setStyleHint(QT_FONT_STYLE_HINTS[self.interface.family])

        self._assign_native(font)

    def load_user_registered_font(self):
        """Use a font that the user has registered in their code."""
        font_key = self.interface._registered_font_key(
            family=self.interface.family,
            weight=self.interface.weight,
            style=self.interface.style,
            variant=self.interface.variant,
        )
        try:
            font_path = _REGISTERED_FONT_CACHE[font_key]
        except KeyError as exc:
            msg = f"{self.interface} not a user-registered font"
            raise UnknownFontError(msg) from exc

        # Find the font family name to use for this font.
        try:
            family_name = _CUSTOM_FONT_NAMES[font_key]
        except KeyError as exc:
            # Font isn't yet loaded into QFontDatabase.
            if not Path(font_path).is_file():
                msg = f"Font file {font_path} could not be found"
                raise ValueError(msg) from exc

            id = QFontDatabase.addApplicationFont(font_path)
            if id == -1:
                msg = f"Unable to load font file {font_path}"
                raise ValueError(msg) from exc

            # Get the family name of the font we just loaded, and remember it.
            family_name = QFontDatabase.applicationFontFamilies(id)[0]
            _CUSTOM_FONT_NAMES[font_path] = family_name

        # Create the font query.
        font = QFont()
        font.setFamily(family_name)
        self._assign_native(font)

    def load_arbitrary_system_font(self):
        """Use a font available on the system."""
        if self.interface.family not in QFontDatabase.families():
            msg = f"{self.interface} not a registered font"
            raise UnknownFontError(msg)
        font = QFont()
        font.setFamily(self.interface.family)
        self._assign_native(font)

    def _assign_native(self, font):
        # Given a minimally initialized QFont, set all the other features
        font.setStyle(QT_FONT_STYLES[self.interface.style])
        weight = QT_FONT_WEIGHTS.get(self.interface.weight, self.interface.weight)
        font.setWeight(weight)
        if self.interface.variant == SMALL_CAPS:
            font.setCapitalization(QFont.Capitalization.SmallCaps)
        if self.interface.size != SYSTEM_DEFAULT_FONT_SIZE:
            font.setPointSizeF(self.interface.size)

        # Set the native font and remember it
        self.native = font
        _IMPL_CACHE[self.interface] = self
