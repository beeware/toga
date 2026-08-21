from travertino.constants import TRANSPARENT
from travertino.size import at_least

from toga.constants import ToggleRole
from toga_cocoa.libs import (
    SEL,
    NSBezelStyle,
    NSButton,
    NSColor,
    NSLayoutAttributeCenterY,
    NSLayoutAttributeLeft,
    NSLayoutAttributeRight,
    NSLayoutConstraint,
    NSLayoutRelationEqual,
    NSOffState,
    NSOnState,
    NSSwitch,
    NSSwitchButton,
    NSTextField,
    objc_method,
    objc_property,
)

from ..colors import native_color
from ..container import TogaView
from .base import Widget


class TogaCheckbox(NSButton):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def onPress_(self, obj) -> None:
        self.interface.on_change()


class TogaSwitch(NSSwitch):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def onPress_(self, obj) -> None:
        self.interface.on_change()


SWITCH_LABEL_GAP = 6
"""Gap, in pixels, between the switch and the label for SWITCH-type Toggles."""


class Toggle(Widget):
    switch_native: TogaSwitch | TogaCheckbox
    label_native: NSTextField | None

    @property
    def role(self):
        role: ToggleRole = self.interface._role
        if role == ToggleRole.AUTOMATIC:
            # Use a checkbox by default on macOS.
            return ToggleRole.CHECKBOX
        return role

    def create(self):
        if self.role == ToggleRole.CHECKBOX:
            self.native = TogaCheckbox.alloc().init()
            self.native.interface = self.interface
            self.native.impl = self
            self.native.bezelStyle = NSBezelStyle.Rounded
            self.native.setButtonType(NSSwitchButton)
            self.switch_native = self.native
            self.label_native = None
        elif self.role == ToggleRole.SWITCH:
            self.native = TogaView.alloc().init()

            self.switch_native = TogaSwitch.alloc().init()
            self.switch_native.interface = self.interface
            self.switch_native.impl = self
            self.switch_native.translatesAutoresizingMaskIntoConstraints = False
            for attribute in (NSLayoutAttributeLeft, NSLayoutAttributeCenterY):
                # Vertically center and left-align the switch
                self.native.addConstraint(
                    NSLayoutConstraint.constraintWithItem(
                        self.native,
                        attribute__1=attribute,
                        relatedBy=NSLayoutRelationEqual,
                        toItem=self.switch_native,
                        attribute__2=attribute,
                    )
                )
            self.native.addSubview(self.switch_native)

            self.label_native = NSTextField.alloc().init()
            self.label_native.drawsBackground = False
            self.label_native.editable = False
            self.label_native.bezeled = False
            self.label_native.translatesAutoresizingMaskIntoConstraints = False
            # Put the label to the right of the switch by SWITCH_LABEL_GAP pixels
            self.native.addConstraint(
                NSLayoutConstraint.constraintWithItem(
                    self.label_native,
                    attribute__1=NSLayoutAttributeLeft,
                    relatedBy=NSLayoutRelationEqual,
                    toItem=self.switch_native,
                    attribute__2=NSLayoutAttributeRight,
                    multiplier=1.0,
                    constant=SWITCH_LABEL_GAP,
                )
            )
            self.native.addConstraint(
                NSLayoutConstraint.constraintWithItem(
                    self.native,
                    attribute__1=NSLayoutAttributeCenterY,
                    relatedBy=NSLayoutRelationEqual,
                    toItem=self.label_native,
                    attribute__2=NSLayoutAttributeCenterY,
                )
            )
            self.native.addSubview(self.label_native)

        self.switch_native.target = self.switch_native
        self.switch_native.action = SEL("onPress:")

        # Add the layout constraints
        self.add_constraints()

    def get_text(self):
        if self.role == ToggleRole.SWITCH:
            return str(self.label_native.stringValue)
        else:
            return str(self.native.title)

    def set_text(self, text):
        if self.role == ToggleRole.SWITCH:
            self.label_native.stringValue = text
        else:
            self.native.title = text

    def set_font(self, font):
        if self.role == ToggleRole.SWITCH:
            self.label_native.font = font._impl.native
        else:
            self.native.font = font._impl.native

    def get_value(self):
        return self.switch_native.state == NSOnState

    def set_value(self, value):
        old_value = self.switch_native.state == NSOnState
        self.switch_native.state = NSOnState if value else NSOffState
        if self.interface.on_change and value != old_value:
            self.interface.on_change()

    def rehint(self):
        if self.role == ToggleRole.SWITCH:
            label_size = self.label_native.intrinsicContentSize()
            switch_size = self.switch_native.intrinsicContentSize()
            width, height = (
                switch_size.width + SWITCH_LABEL_GAP + label_size.width,
                max(switch_size.height, label_size.height),
            )
        else:
            content_size = self.native.intrinsicContentSize()
            width, height = content_size.width, content_size.height
        self.interface.intrinsic.width = at_least(width)
        self.interface.intrinsic.height = height

    def set_background_color(self, color):
        if color == TRANSPARENT:
            # macOS bug: even when drawsBackground=False,
            # background color still seems drawn in certain
            # cases.
            self.native.backgroundColor = NSColor.clearColor
            self.native.drawsBackground = False
        else:
            self.native.backgroundColor = native_color(color)
            self.native.drawsBackground = True
