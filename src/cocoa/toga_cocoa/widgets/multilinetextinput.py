from toga_cocoa.libs import *

from .base import Widget


class TogaTextView(NSTextView):
    @objc_method
    def touchBar(self):
        # Disable the touchbar.
        return None


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
        self.text = TogaTextView.alloc().init()
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
        self.text.placeholderString = self.interface._value

    def set_readonly(self, value):
        self.text.editable = not self.interface._readonly

    def set_value(self, value):
        self.text.string = self.interface._value

    def apply_sub_layout(self):
        self._width_constraint.constant = self.interface.layout.width
        self._height_constraint.constant = self.interface.layout.height

    def rehint(self):
        self.interface.style.hint(
            min_height=100,
            min_width=100
        )
