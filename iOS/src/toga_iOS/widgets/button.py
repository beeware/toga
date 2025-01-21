from rubicon.objc import SEL, CGSize, objc_method, objc_property
from travertino.size import at_least

from toga.colors import TRANSPARENT
from toga_iOS.colors import native_color
from toga_iOS.libs import (
    UIButton,
    UIColor,
    UIControlEventTouchDown,
    UIControlStateDisabled,
    UIControlStateNormal,
)
from toga_iOS.widgets.base import Widget


class TogaButton(UIButton):
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

        self.native.setTitleColor(self.native.tintColor, forState=UIControlStateNormal)
        self.native.setTitleColor(UIColor.grayColor, forState=UIControlStateDisabled)
        self.native.addTarget(
            self.native,
            action=SEL("onPress:"),
            forControlEvents=UIControlEventTouchDown,
        )

        self._icon = None

        # Add the layout constraints
        self.add_constraints()

    def get_text(self):
        return str(self.native.titleForState(UIControlStateNormal))

    def set_text(self, text):
        self.native.setTitle(text, forState=UIControlStateNormal)

    def get_icon(self):
        return self._icon

    def set_icon(self, icon):
        self._icon = icon
        if icon:
            self.native.setImage(icon._impl._as_size(48), forState=UIControlStateNormal)
        else:
            self.native.setImage(None, forState=UIControlStateNormal)

    def set_color(self, color):
        if color is None:
            self.native.setTitleColor(
                self.native.tintColor, forState=UIControlStateNormal
            )
        else:
            self.native.setTitleColor(
                native_color(color), forState=UIControlStateNormal
            )

    def set_background_color(self, color):
        if color == TRANSPARENT or color is None:
            self.native.backgroundColor = None
        else:
            self.native.backgroundColor = native_color(color)

    def set_font(self, font):
        self.native.titleLabel.font = font._impl.native

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        # print(f"REHINT BUTTON {fitting_size.width}x{fitting_size.height}")
        self.interface.intrinsic.width = at_least(fitting_size.width)
        self.interface.intrinsic.height = fitting_size.height
