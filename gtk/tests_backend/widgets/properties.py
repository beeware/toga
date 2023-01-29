from dataclasses import dataclass

from toga.fonts import NORMAL
from toga.style.pack import CENTER, JUSTIFY, LEFT, RIGHT
from toga_gtk.libs import Gtk, Pango


def toga_color(color):
    return color


@dataclass
class Font:
    family: str
    size: int
    style: str = NORMAL
    variant: str = NORMAL
    weight: str = NORMAL


def toga_font(font):
    return Font(
        family=font.get_family(),
        size=font.get_size() / Pango.SCALE,
    )


def toga_alignment(alignment):
    return {
        (0.0, Gtk.Justification.LEFT): LEFT,
        (1.0, Gtk.Justification.RIGHT): RIGHT,
        (0.5, Gtk.Justification.CENTER): CENTER,
        (0.0, Gtk.Justification.FILL): JUSTIFY,
    }[alignment]
