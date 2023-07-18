from abc import abstractmethod

from toga.constants import CENTER, JUSTIFY, LEFT, RIGHT, TRANSPARENT

from ..colors import native_color
from ..libs.activity import MainActivity
from ..libs.android.graphics import PorterDuff__Mode, PorterDuffColorFilter, Rect
from ..libs.android.graphics.drawable import ColorDrawable, InsetDrawable
from ..libs.android.view import Gravity, View


def _get_activity(_cache=[]):
    """Android Toga widgets need a reference to the current activity to pass it as
    `context` when creating Android native widgets. This may be useful at any time, so
    we retain a global JNI ref.

    :param _cache: List that is either empty or contains 1 item, the cached global JNI ref
    """
    if _cache:
        return _cache[0]
    # See MainActivity.onCreate() for initialization of .singletonThis:
    # https://github.com/beeware/briefcase-android-gradle-template/blob/3.7/%7B%7B%20cookiecutter.formal_name%20%7D%7D/app/src/main/java/org/beeware/android/MainActivity.java
    # This can't be tested because if it isn't set, nothing else will work.
    if not MainActivity.singletonThis:  # pragma: no cover
        raise ValueError(
            "Unable to find MainActivity.singletonThis from Python. This is typically set by "
            "org.beeware.android.MainActivity.onCreate()."
        )
    _cache.append(MainActivity.singletonThis.__global__())
    return _cache[0]


class Widget:
    # Some widgets are not generally focusable, but become focusable if there has been a
    # keyboard event since the last touch event. To avoid this complicating the tests,
    # these widgets disable programmatic focus entirely by setting focusable = False.
    focusable = True

    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.interface._impl = self
        self._container = None
        self.native = None
        self._native_activity = _get_activity()
        self.create()
        # Immediately re-apply styles. Some widgets may defer style application until
        # they have been added to a container.
        self.interface.style.reapply()

    @abstractmethod
    def create(self):
        ...

    def set_app(self, app):
        pass

    def set_window(self, window):
        pass

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, container):
        if self._container:
            self._container.remove_content(self)

        self._container = container
        if container:
            container.add_content(self)

        for child in self.interface.children:
            child._impl.container = container

        self.rehint()

    @property
    def viewport(self):
        return self._container

    # Convert CSS pixels to native pixels
    def scale_in(self, value):
        return int(round(value * self.container.scale))

    # Convert native pixels to CSS pixels
    def scale_out(self, value):
        return int(round(value / self.container.scale))

    def get_enabled(self):
        return self.native.isEnabled()

    def set_enabled(self, value):
        self.native.setEnabled(value)

    def focus(self):
        if self.focusable:
            self.native.requestFocus()

    def get_tab_index(self):
        self.interface.factory.not_implemented("Widget.get_tab_index()")

    def set_tab_index(self, tab_index):
        self.interface.factory.not_implemented("Widget.set_tab_index()")

    # APPLICATOR

    def set_bounds(self, x, y, width, height):
        self.container.set_content_bounds(self, x, y, width, height)

    def set_hidden(self, hidden):
        if hidden:
            self.native.setVisibility(View.INVISIBLE)
        else:
            self.native.setVisibility(View.VISIBLE)

    def set_font(self, font):
        # By default, font can't be changed
        pass

    # Although setBackgroundColor is defined in the View base class, we can't use it as
    # a default implementation because it often overwrites other aspects of the widget's
    # appearance. So each widget must decide how to implement this method, possibly
    # using one of the utility functions below.
    def set_background_color(self, color):
        pass

    def set_background_simple(self, value):
        if not hasattr(self, "_default_background"):
            self._default_background = self.native.getBackground()

        if value in (None, TRANSPARENT):
            self.native.setBackground(self._default_background)
        else:
            background = ColorDrawable(native_color(value))
            if isinstance(self._default_background, InsetDrawable):
                outer_padding = Rect()
                inner_padding = Rect()
                self._default_background.getPadding(outer_padding)
                self._default_background.getDrawable().getPadding(inner_padding)
                insets = [
                    getattr(outer_padding, name) - getattr(inner_padding, name)
                    for name in ["left", "top", "right", "bottom"]
                ]
                background = InsetDrawable(background, *insets)
            self.native.setBackground(background)

    def set_background_filter(self, value):
        self.native.getBackground().setColorFilter(
            None
            if value in (None, TRANSPARENT)
            else PorterDuffColorFilter(native_color(value), PorterDuff__Mode.SRC_IN)
        )

    def set_alignment(self, alignment):
        pass  # If appropriate, a widget subclass will implement this.

    def set_color(self, color):
        pass  # If appropriate, a widget subclass will implement this.

    # INTERFACE

    def add_child(self, child):
        child.container = self.container

    def insert_child(self, index, child):
        self.add_child(child)

    def remove_child(self, child):
        child.container = None

    def refresh(self):
        self.rehint()

    @abstractmethod
    def rehint(self):
        pass


def align(value):
    """Convert toga alignment values into Android alignment values."""
    return {
        LEFT: Gravity.LEFT,
        RIGHT: Gravity.RIGHT,
        CENTER: Gravity.CENTER_HORIZONTAL,
        JUSTIFY: Gravity.LEFT,
    }[value]
