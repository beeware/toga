from toga.constants import *


def gtk_alignment(alignment):
    "Convert Toga alignments in to arguments compatible with Gtk.set_alignment"
    return {
        LEFT_ALIGNMENT: (0.0, 0.5),
        RIGHT_ALIGNMENT: (1.0, 0.5),
        CENTER_ALIGNMENT: (0.5, 0.5),
        JUSTIFIED_ALIGNMENT: (0.0, 0.0),
        NATURAL_ALIGNMENT: (0.0, 0.5),
    }[alignment]
