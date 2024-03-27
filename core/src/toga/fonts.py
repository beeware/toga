from __future__ import annotations

from pathlib import Path

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
        """Constructs a reference to a font.

        This class should be used when an API requires an explicit font reference (e.g.
        :any:`Context.write_text`). In all other cases, fonts in Toga are controlled
        using the style properties linked below.

        :param family: The :ref:`font family <pack-font-family>`.
        :param size: The :ref:`font size <pack-font-size>`.
        :param weight: The :ref:`font weight <pack-font-weight>`.
        :param style: The :ref:`font style <pack-font-style>`.
        :param variant: The :ref:`font variant <pack-font-variant>`.
        """
        super().__init__(family, size, weight=weight, style=style, variant=variant)
        self.factory = get_platform_factory()
        self._impl = self.factory.Font(self)

    def __str__(self) -> str:
        size = (
            "default size"
            if self.size == SYSTEM_DEFAULT_FONT_SIZE
            else f"{self.size}pt"
        )
        weight = f" {self.weight}" if self.weight != NORMAL else ""
        variant = f" {self.variant}" if self.variant != NORMAL else ""
        style = f" {self.style}" if self.style != NORMAL else ""
        return f"{self.family} {size}{weight}{variant}{style}"

    @staticmethod
    def register(
        family: str,
        path: str | Path,
        *,
        weight: str = NORMAL,
        style: str = NORMAL,
        variant: str = NORMAL,
    ) -> None:
        """Registers a file-based font.

        **Note:** This is not currently supported on macOS or iOS.

        :param family: The :ref:`font family <pack-font-family>`.
        :param path: The path to the font file. This can be an absolute path, or a path
            relative to the module that defines your :any:`App` class.
        :param weight: The :ref:`font weight <pack-font-weight>`.
        :param style: The :ref:`font style <pack-font-style>`.
        :param variant: The :ref:`font variant <pack-font-variant>`.
        """
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
