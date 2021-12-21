from typing import Callable
from inspect import ismethod
from rubicon.java.jni import java
from toga.constants import CENTER, JUSTIFY, LEFT, RIGHT

from ..libs.activity import MainActivity
from ..libs.android.view import Gravity


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
        self.deferred_execution = [False, []]
        """
        [whether_execuate_now, (method, args, kargs)]
        for defered excecution of methods which need access to activity,
        because the activity can not be got until onCreate event.

        When activity is got, `replay` method will be called and 
        defered methods will be executed.
        """
        self.native = None
        self.interface = interface
        self.interface._impl = self
        self._container = None
        self._native_activity = None
        self.create()

    def __getattribute__(self, name):
        """
        It is a hack for lazy execution which access the Activity.
        """
        deferred_execution = object.__getattribute__(self, "deferred_execution")
        member = object.__getattribute__(self, name)
        if deferred_execution[0] or not ismethod(member):
            return member
        if name == "replay_deferred_methods" or name.startswith("__"):
            return member

        def defered_method(*args, **kargs):
            if deferred_execution[0]:
                return member(*args, **kargs)
            deferred_execution[1].append((member, args, kargs))

        return defered_method

    # execute the defered methods
    def replay_deferred_methods(self, native_activity):
        self._native_activity = native_activity
        for child in self.interface.children:
            child._impl.replay_deferred_methods(native_activity)
        self.deferred_execution[0] = True
        for method, x, y in self.deferred_execution[1]:
            print("execute: ", method, x, y)
            method(*x, **y)
        self.deferred_execution[1].clear()
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
        self.set_container(container)

    def set_container(self, container):
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
        self.native.requestFocus()

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
