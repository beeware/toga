import weakref

from toga.constants import CENTER, JUSTIFY, LEFT, RIGHT

from . import Gtk
from .gtk import GTK_VERSION


def gtk_text_align(alignment):
    """Convert Toga text alignments into arguments compatible with Gtk."""
    return {
        LEFT: (0.0, Gtk.Justification.LEFT),
        RIGHT: (1.0, Gtk.Justification.RIGHT),
        CENTER: (0.5, Gtk.Justification.CENTER),
        JUSTIFY: (0.0, Gtk.Justification.FILL),
    }[alignment]


if GTK_VERSION >= (4, 0, 0):  # pragma: no-cover-if-gtk3

    def create_toga_native(native_gtk_class):  # pragma: no-cover-if-gtk3
        """Create a new native class from a native gtk class, whose virtual functions
        could be safely overridden."""
        toga_native_class = type(
            native_gtk_class.__gtype__.name,
            (native_gtk_class,),
            {"base_class": native_gtk_class},  # Store the base class type
        )
        return toga_native_class

    class WeakrefCallable:  # pragma: no-cover-if-gtk3
        """
        A wrapper for callable that holds a weak reference to it.

        This can be useful in particular when setting gtk virtual function handlers,
        to avoid cyclical reference cycles between python and gi that are detected
        neither by the python garbage collector nor the gi.
        """

        def __init__(self, function):
            try:
                self.ref = weakref.WeakMethod(function)
            except TypeError:  # pragma: no cover
                self.ref = weakref.ref(function)

        def __call__(self, *args, **kwargs):
            function = self.ref()
            if function:  # pragma: no branch
                return function(*args, **kwargs)
