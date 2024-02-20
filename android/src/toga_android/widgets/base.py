from abc import ABC, abstractmethod
from decimal import ROUND_HALF_EVEN, Decimal

from android.graphics import PorterDuff, PorterDuffColorFilter, Rect
from android.graphics.drawable import ColorDrawable, InsetDrawable
from android.view import Gravity, View
from android.widget import RelativeLayout
from org.beeware.android import MainActivity
from travertino.size import at_least

from toga.constants import CENTER, JUSTIFY, LEFT, RIGHT, TRANSPARENT

from ..colors import native_color


class Scalable:
    SCALE_DEFAULT_ROUNDING = ROUND_HALF_EVEN

    def init_scale(self, context):
        # The baseline DPI is 160:
        # https://developer.android.com/training/multiscreen/screendensities
        self.dpi_scale = context.getResources().getDisplayMetrics().densityDpi / 160

    # Convert CSS pixels to native pixels
    def scale_in(self, value, rounding=SCALE_DEFAULT_ROUNDING):
        return self.scale_round(value * self.dpi_scale, rounding)

    # Convert native pixels to CSS pixels
    def scale_out(self, value, rounding=SCALE_DEFAULT_ROUNDING):
        if isinstance(value, at_least):
            return at_least(self.scale_out(value.value, rounding))
        else:
            return self.scale_round(value / self.dpi_scale, rounding)

    def scale_round(self, value, rounding):
        if rounding is None:  # pragma: no cover
            return value
        return int(Decimal(value).to_integral(rounding))


class Widget(ABC, Scalable):
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
        self._native_activity = MainActivity.singletonThis
        self.init_scale(self._native_activity)
        self.create()

        # Some widgets, e.g. TextView, may throw an exception if we call measure()
        # before setting LayoutParams.
        self.native.setLayoutParams(
            RelativeLayout.LayoutParams(
                RelativeLayout.LayoutParams.WRAP_CONTENT,
                RelativeLayout.LayoutParams.WRAP_CONTENT,
            )
        )

        # Immediately re-apply styles. Some widgets may defer style application until
        # they have been added to a container.
        self.interface.style.reapply()

    @abstractmethod
    def create(self): ...

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

        self.refresh()

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
        self.container.set_content_bounds(
            self, *map(self.scale_in, (x, y, width, height))
        )

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
            else PorterDuffColorFilter(native_color(value), PorterDuff.Mode.SRC_IN)
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

    # TODO: consider calling requestLayout or forceLayout here
    # (https://github.com/beeware/toga/issues/1289#issuecomment-1453096034)
    def refresh(self):
        # Default values; may be overwritten by rehint().
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
        self.rehint()

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
