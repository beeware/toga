from toga.constants import CENTER, JUSTIFY, LEFT, RIGHT

from ..libs.activity import MainActivity
from ..libs.android.view import Gravity, View


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
    if not MainActivity.singletonThis:
        raise ValueError("Unable to find MainActivity.singletonThis from Python. This is typically set by "
                         "org.beeware.android.MainActivity.onCreate().")
    _cache.append(MainActivity.singletonThis.__global__())
    return _cache[0]


class Widget:
    def __init__(self, interface):
        self.interface = interface
        self.interface._impl = self
        self._container = None
        self.viewport = None
        self.native = None
        self._native_activity = _get_activity()
        self.create()
        # Immediately re-apply styles. Some widgets may defer style application until
        # they have been added to a container.
        self.interface.style.reapply()

    def create(self):
        pass

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        if self.container:
            if container:
                raise RuntimeError('Already have a container')
            else:
                # container is set to None, removing self from the container.native
                self._container.native.removeView(self.native)
                self._container.native.invalidate()
                self._container = None
        elif container:
            self._container = container
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
        self.native.requestFocus()

    # APPLICATOR

    def set_bounds(self, x, y, width, height):
        if self.container:
            # Ask the container widget to set our bounds.
            self.container.set_child_bounds(self, x, y, width, height)

    def set_hidden(self, hidden):
        view = View(self._native_activity)
        if not view.getClass().isInstance(self.native):
            # save guard for Widgets like Canvas that are not based on View
            self.interface.factory.not_implemented("Widget.set_hidden()")
            return
        if hidden:
            self.native.setVisibility(View.INVISIBLE)
        else:
            self.native.setVisibility(View.VISIBLE)

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
        if self.viewport:
            # we are the top level widget
            child.container = self
        else:
            child.container = self.container

    def insert_child(self, index, child):
        self.add_child(child)

    def remove_child(self, child):
        child.container = None

    def rehint(self):
        pass


def align(value):
    """Convert toga alignment values into Android alignment values"""
    return {
        LEFT: Gravity.LEFT,
        RIGHT: Gravity.RIGHT,
        CENTER: Gravity.CENTER_HORIZONTAL,
        JUSTIFY: Gravity.LEFT,
    }[value]
