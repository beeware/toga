from abc import ABC, abstractmethod
from decimal import ROUND_HALF_EVEN, Decimal

from android.graphics import PorterDuff, PorterDuffColorFilter
from android.graphics.drawable import ColorDrawable
from android.view import Gravity, View
from android.widget import RelativeLayout
from org.beeware.android import MainActivity
from travertino.size import at_least

from toga.colors import TRANSPARENT
from toga.constants import CENTER, JUSTIFY, LEFT, RIGHT
from toga_android.colors import native_color


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

        self.native_toplevel = self.native

        # Some widgets, e.g. TextView, may throw an exception if we call measure()
        # before setting LayoutParams.
        self.native.setLayoutParams(
            RelativeLayout.LayoutParams(
                RelativeLayout.LayoutParams.WRAP_CONTENT,
                RelativeLayout.LayoutParams.WRAP_CONTENT,
            )
        )

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
            self.native_toplevel.setVisibility(View.INVISIBLE)
        else:
            self.native_toplevel.setVisibility(View.VISIBLE)

    def set_font(self, font):
        # By default, font can't be changed
        pass

    def set_background_color(self, color):
        # Set background to None, when TRANSPARENT is requested, in order to prevent
        # clipping of ripple and other effects on widgets.
        self.native_toplevel.setBackground(
            None if color in (None, TRANSPARENT) else ColorDrawable(native_color(color))
        )

    def set_background_filter(self, color):
        # Although setBackgroundColor is defined in the View base class, we can't
        # use it as a default implementation on some widgets (e.g. Button), because
        # it often overwrites other aspects of the widget's appearance. For example,
        # when setBackgroundColor is used on a Button, it makes the button appear
        # as a solid rectangle with no bevels or animations.
        self.native.getBackground().setColorFilter(
            None
            if color is None
            else PorterDuffColorFilter(native_color(color), PorterDuff.Mode.SRC_IN)
        )

    def set_text_align(self, alignment):
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


def android_text_align(value):
    """Convert toga alignment values into Android alignment values."""
    return {
        LEFT: Gravity.LEFT,
        RIGHT: Gravity.RIGHT,
        CENTER: Gravity.CENTER_HORIZONTAL,
        JUSTIFY: Gravity.LEFT,
    }[value]


# The look and feel of Android widgets is sometimes implemented using background
# Drawables like ColorDrawable, InsetDrawable and other animation effect Drawables
# like RippleDrawable. Often when such effect Drawables are used, they are stacked
# along with other Drawables in a LayerDrawable.
#
# LayerDrawable once created cannot be modified and attempting to modify it or
# creating a new LayerDrawable using the elements of the original LayerDrawable
# stack, will destroy the native look and feel of the widgets. The original
# LayerDrawable cannot also be properly cloned. Using `getConstantState()` on the
# Drawable will produce an erroneous version of the original Drawable.
#
# Hence, the best option to preserve the native look and feel of the these widgets is
# to contain them in a `RelativeLayout` and set the background color to the layout
# instead of the widget itself.
#
# ContainedWidget should act as a drop-in replacement against the Widget class for
# such widgets, without requiring the widgets to do anything extra on their part.
class ContainedWidget(Widget):
    def __init__(self, interface):
        super().__init__(interface)

        self.native_toplevel = RelativeLayout(self._native_activity)
        self.native_toplevel.addView(self.native)

        self.native.setLayoutParams(
            RelativeLayout.LayoutParams(
                RelativeLayout.LayoutParams.MATCH_PARENT,
                RelativeLayout.LayoutParams.MATCH_PARENT,
            )
        )
