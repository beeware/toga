from travertino.fonts import Font

from toga.colors import rgba
from toga.style.pack import CENTER, JUSTIFY, LEFT, RIGHT
from toga_gtk.libs import Gtk, Pango


def toga_color(color):
    if color:
        return rgba(
            int(color.red * 255),
            int(color.green * 255),
            int(color.blue * 255),
            color.alpha,
        )
    else:
        return None


def toga_font(font):
    return Font(
        family=font.get_family(),
        size=int(font.get_size() / Pango.SCALE),
    )


def toga_alignment(alignment):
    return {
        (0.0, Gtk.Justification.LEFT): LEFT,
        (1.0, Gtk.Justification.RIGHT): RIGHT,
        (0.5, Gtk.Justification.CENTER): CENTER,
        (0.0, Gtk.Justification.FILL): JUSTIFY,
    }[alignment]
