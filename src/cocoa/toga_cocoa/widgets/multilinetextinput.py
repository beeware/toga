from travertino.size import at_least

from toga_cocoa.libs import *

from .base import Widget


class MultilineTextInput(Widget):
    def create(self):
        # Create a multiline view, and put it in a scroll view.
        # The scroll view is the native, because it's the outer container.
        self.native = NSScrollView.alloc().init()
        self.native.hasVerticalScroller = True
        self.native.hasHorizontalScroller = False
        self.native.autohidesScrollers = False
        self.native.borderType = NSBezelBorder

        # Disable all autolayout functionality on the outer widget
        self.native.translatesAutoresizingMaskIntoConstraints = False
        self.native.autoresizesSubviews = True

        # Create the actual text widget
        self.text = NSTextView.alloc().init()
        self.text.editable = True
        self.text.selectable = True
        self.text.verticallyResizable = True
        self.text.horizontallyResizable = False

        # Disable the autolayout functionality, and replace with
        # constraints controlled by the layout.
        self.text.translatesAutoresizingMaskIntoConstraints = False
        self._width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.text, NSLayoutAttributeRight,
            NSLayoutRelationEqual,
            self.text, NSLayoutAttributeLeft,
            1.0, 0
        )
        self.text.addConstraint(self._width_constraint)

        self._height_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.text, NSLayoutAttributeBottom,
            NSLayoutRelationEqual,
            self.text, NSLayoutAttributeTop,
            1.0, 0
        )
        self.text.addConstraint(self._height_constraint)

        # Put the text view in the scroll window.
        self.native.documentView = self.text

        # Add the layout constraints
        self.add_constraints()

    def set_placeholder(self, value):
        self.text.placeholderString = value

    def set_readonly(self, value):
        self.text.editable = not value

    def set_value(self, value):
        self.text.string = value

    def _update_child_layout(self):
        self._width_constraint.constant = self.interface.layout.width
        self._height_constraint.constant = self.interface.layout.height

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
