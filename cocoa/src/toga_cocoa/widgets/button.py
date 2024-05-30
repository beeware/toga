from rubicon.objc import SEL, objc_method, objc_property
from travertino.size import at_least

from toga.colors import TRANSPARENT
from toga.fonts import SYSTEM_DEFAULT_FONT_SIZE
from toga.style.pack import NONE
from toga_cocoa.colors import native_color
from toga_cocoa.libs import (
    NSBezelStyle,
    NSButton,
    NSMomentaryPushInButton,
)

from .base import Widget


class TogaButton(NSButton):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def onPress_(self, obj) -> None:
        self.interface.on_press()


class Button(Widget):
    def create(self):
        self.native = TogaButton.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self

        self._icon = None

        self.native.buttonType = NSMomentaryPushInButton
        self._set_button_style()

        self.native.target = self.native
        self.native.action = SEL("onPress:")

        # Add the layout constraints
        self.add_constraints()

    def _set_button_style(self):
        # Normal Cocoa "rounded" buttons have a fixed height by definition.
        # If the user specifies any font size other than the default,
        # or specifies an explicit height for layout, switch to using a
        # RegularSquare button.
        if (
            self.interface.style.font_size != SYSTEM_DEFAULT_FONT_SIZE
            or self.interface.style.height != NONE
            or self._icon is not None
        ):
            self.native.bezelStyle = NSBezelStyle.RegularSquare
        else:
            self.native.bezelStyle = NSBezelStyle.Rounded

    def set_bounds(self, x, y, width, height):
        # Button style is sensitive to height. If the bounds have changed,
        # there has possibly been a height change; Ensure that the button's
        # style is updated.
        self._set_button_style()
        super().set_bounds(x, y, width, height)

    def set_font(self, font):
        self.native.font = font._impl.native

        # Button style is sensitive to font changes
        self._set_button_style()

    def get_text(self):
        return str(self.native.title)

    def set_text(self, text):
        self.native.title = text

    def get_icon(self):
        return self._icon

    def set_icon(self, icon):
        self._icon = icon
        if icon:
            self.native.image = icon._impl._as_size(32)
        else:
            self.native.image = None

        # Button style is sensitive to whether an icon is being used
        self._set_button_style()

    def set_background_color(self, color):
        if color == TRANSPARENT or color is None:
            self.native.bezelColor = None
        else:
            self.native.bezelColor = native_color(color)

    def rehint(self):
        content_size = self.native.intrinsicContentSize()
        self.interface.intrinsic.width = at_least(content_size.width)
        self.interface.intrinsic.height = content_size.height
