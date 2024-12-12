from toga.constants import CENTER, JUSTIFY, LEFT, RIGHT

from . import Gtk


def gtk_text_align(alignment):
    """Convert Toga text alignments into arguments compatible with Gtk."""
    return {
        LEFT: (0.0, Gtk.Justification.LEFT),
        RIGHT: (1.0, Gtk.Justification.RIGHT),
        CENTER: (0.5, Gtk.Justification.CENTER),
        JUSTIFY: (0.0, Gtk.Justification.FILL),
    }[alignment]
