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


def create_toga_native(native_gtk_class):  # pragma: no-cover-if-gtk3
    """Create a new native class from a native gtk class, whose virtual functions
    could be safely overridden."""
    toga_native_class = type(
        native_gtk_class.__gtype__.name,
        (native_gtk_class,),
        {"base_class": native_gtk_class},  # Store the base class type
    )
    return toga_native_class
