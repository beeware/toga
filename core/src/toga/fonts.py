from __future__ import annotations

from pathlib import Path
from typing import Any

# Use the Travertino font definitions as-is
from travertino import constants
from travertino.constants import (
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
)
from travertino.fonts import Font as BaseFont

import toga
from toga.platform import get_platform_factory

SYSTEM_DEFAULT_FONTS = {SYSTEM, MESSAGE, SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE}
SYSTEM_DEFAULT_FONT_SIZE = -1
FONT_WEIGHTS = {NORMAL, BOLD}
FONT_STYLES = {NORMAL, ITALIC, OBLIQUE}
FONT_VARIANTS = {NORMAL, SMALL_CAPS}

_REGISTERED_FONT_CACHE: dict[tuple[str, str, str, str], str] = {}
_IMPL_CACHE: dict[Font, Any] = {}


class UnknownFontError(Exception):
    """Raised when an unknown font family is requested."""


class Font(BaseFont):
    def __init__(
        self,
        family: str,
        size: int | str,
        *,
        weight: str = NORMAL,
        style: str = NORMAL,
        variant: str = NORMAL,
    ):
        """Construct a reference to a font.

        This class should be used when an API requires an explicit font reference (e.g.
        [`Context.write_text`][toga.widgets.canvas.Context.write_text]). In all other
        cases, fonts in Toga are controlled
        using the style properties linked below.

        :param family: The [font family][toga.style.pack.Pack.font_family].
        :param size: The [font size][toga.style.pack.Pack.font_size].
        :param weight: The [font weight][toga.style.pack.Pack.font_weight].
        :param style: The [font style][toga.style.pack.Pack.font_style].
        :param variant: The [font variant][toga.style.pack.Pack.font_variant].

        :raises UnknownFontError: If the font family requested corresponds to neither
            one of the [built-in system fonts][toga.style.pack.Pack.font_family], nor a
            user-registered font, nor (depending on platform) a font installed on the
            system.
        :raises ValueError: If a user-registered font is used, but the file specified
            either doesn't exist or a font can't be successfully loaded from it.
        """
        super().__init__(family, size, weight=weight, style=style, variant=variant)
        self.factory = get_platform_factory()

        try:
            self._impl = _IMPL_CACHE[self]

        except KeyError:
            self._impl = self.factory.Font(self)
            try:
                self._impl.load_predefined_system_font()
            except UnknownFontError:
                try:
                    self._impl.load_user_registered_font()
                except UnknownFontError:
                    try:
                        self._impl.load_arbitrary_system_font()
                    except UnknownFontError as exc:
                        raise UnknownFontError(f"Unknown font '{self}'") from exc

    def __str__(self) -> str:
        size = (
            "default size"
            if self.size == SYSTEM_DEFAULT_FONT_SIZE
            else f"{self.size}pt"
        )
        string = f"{self.family} {size} {self.weight} {self.variant} {self.style}"
        return string.replace(" normal", "")

    @staticmethod
    def register(
        family: str,
        path: str | Path,
        *,
        weight: str = NORMAL,
        style: str = NORMAL,
        variant: str = NORMAL,
    ) -> None:
        """Register a file-based font.

        :param family: The [font family][toga.style.pack.Pack.font_family].
        :param path: The path to the font file. This can be an absolute path, or a path
            relative to the module that defines your [`App`][toga.App] class.
        :param weight: The [font weight][toga.style.pack.Pack.font_weight].
        :param style: The [font style][toga.style.pack.Pack.font_style].
        :param variant: The [font variant][toga.style.pack.Pack.font_variant].
            relative to the module that defines your :any:`App` class.

        :raises ValueError: When the registered family has the same name as the standard
            font families ``"cursive"``, ``"fantasy"``, ``"message"``, ``"monospace"``,
            `"sans-serif"``, "serif", or "system".
        """
        if family in (
            CURSIVE,
            FANTASY,
            MESSAGE,
            MONOSPACE,
            SANS_SERIF,
            SERIF,
            SYSTEM,
        ):
            raise ValueError(
                "Custom fonts cannot be registered with a built-in font family name"
            )
        font_key = Font._registered_font_key(family, weight, style, variant)
        _REGISTERED_FONT_CACHE[font_key] = str(toga.App.app.paths.app / path)

    @staticmethod
    def _registered_font_key(
        family: str,
        weight: str,
        style: str,
        variant: str,
    ) -> tuple[str, str, str, str]:
        if weight not in constants.FONT_WEIGHTS:
            weight = NORMAL
        if style not in constants.FONT_STYLES:
            style = NORMAL
        if variant not in constants.FONT_VARIANTS:
            variant = NORMAL

        return family, weight, style, variant
