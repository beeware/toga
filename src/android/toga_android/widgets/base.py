from ..libs.activity import MainActivity
from ..libs.android_widgets import Gravity

from rubicon.java.jni import java

from toga.constants import CENTER, JUSTIFY, LEFT, RIGHT


def _get_activity(_cache=[]):
    """
    Android Toga widgets need a reference to the current activity to pass it as `context` when creating
    Android native widgets. This may be useful at any time, so we retain a global JNI ref.

    :param _cache: List that is either empty or contains 1 item, the cached global JNI ref
    """
    if _cache:
        return _cache[0]
    # See MainActivity.onCreate() for initialization of .singletonThis:
    # https://github.com/beeware/briefcase-android-gradle-template/blob/3.7/%7B%7B%20cookiecutter.formal_name%20%7D%7D/app/src/main/java/org/beeware/android/MainActivity.java
    if MainActivity.singletonThis is None:
        raise ValueError("Unable to find MainActivity.singletonThis from Python. This is typically set by "
                         "org.beeware.android.MainActivity.onCreate().")
    _cache.append(MainActivity(__jni__=java.NewGlobalRef(MainActivity.singletonThis)))
    return _cache[0]


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._container = None
        self.native = None
        self._native_activity = _get_activity()
        self.create()
        # Immediately re-apply styles. Some widgets may defer style application until
        # they have been added to a container.
        self.interface.style.reapply()

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        self._container = container
        self.viewport = container.viewport

        if self.native:
            # When initially setting the container and adding widgets to the container,
            # we provide no `LayoutParams`. Those are promptly added when Toga
            # calls `widget.rehint()` and `widget.set_bounds()`.
            self._container.native.addView(self.native)

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    def set_enabled(self, value):
        self.native.setEnabled(value)

    def focus(self):
        self.interface.factory.not_implemented("Widget.focus()")

    # APPLICATOR

    def set_bounds(self, x, y, width, height):
        if self.container:
            # Ask the container widget to set our bounds.
            self.container.set_child_bounds(self, x, y, width, height)

    def set_hidden(self, hidden):
        self.interface.factory.not_implemented("Widget.set_hidden()")

    def set_font(self, font):
        # By default, font can't be changed
        pass

    def set_background_color(self, color):
        # By default, background color can't be changed.
        pass

    def set_alignment(self, alignment):
        pass  # If appropriate, a widget subclass will implement this.

    def set_color(self, color):
        pass  # If appropriate, a widget subclass will implement this.

    # INTERFACE

    def add_child(self, child):
        if self.container:
            child.viewport = self.root.viewport
            child.container = self.container

    def rehint(self):
        pass


def align(value):
    """Convert toga alignment values into Android alignment values"""
    return {
        LEFT: Gravity.LEFT,
        RIGHT: Gravity.RIGHT,
        CENTER: Gravity.CENTER_HORIZONTAL,
        JUSTIFY: Gravity.CENTER_HORIZONTAL,
    }[value]
