from toga.constants import *


try:
    text = unicode
except NameError:
    text = str


def gtk_alignment(alignment):
    "Convert Toga alignments in to arguments compatible with Gtk.set_alignment"
    return {
        LEFT: (0.0, 0.5),
        RIGHT: (1.0, 0.5),
        CENTER: (0.5, 0.5),
        JUSTIFY: (0.0, 0.0),
    }[alignment]
