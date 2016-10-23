from toga.constants import *


try:
    text = unicode
except NameError:
    text = str


def gtk_alignment(alignment):
    "Convert Toga alignments in to arguments compatible with Gtk.set_alignment"
    return {
        LEFT_ALIGNED: (0.0, 0.5),
        RIGHT_ALIGNED: (1.0, 0.5),
        CENTER_ALIGNED: (0.5, 0.5),
        JUSTIFIED_ALIGNED: (0.0, 0.0),
        NATURAL_ALIGNED: (0.0, 0.5),
    }[alignment]
