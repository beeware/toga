from rubicon.objc import CGPoint, objc_method, objc_property
from travertino.size import at_least

from toga_iOS.libs import (
    NSLayoutAttributeBottom,
    NSLayoutAttributeLeading,
    NSLayoutAttributeTop,
    NSLayoutAttributeTrailing,
    NSLayoutConstraint,
    NSLayoutRelationEqual,
    UILabel,
    UITextView
)
from toga_iOS.widgets.base import Widget


class TogaMultilineTextView(UITextView):

    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def pointInside_withEvent_(self, point: CGPoint, event) -> bool:
        # To keep consistency with non-mobile platforms, we'll resign the
        # responder status when you tap somewhere else outside this view
        # (except the keyboard)
        within_x = point.x > 0 and point.x < self.frame.size.width
        within_y = point.y > 0 and point.y < self.frame.size.height
        in_view = within_x and within_y
        if not in_view:
            self.resignFirstResponder()
        return in_view

    @objc_method
    def textViewShouldEndEditing_(self, text_view):
        return True

    @objc_method
    def textViewDidBeginEditing_(self, text_view):
        self.placeholder_label.setHidden_(True)

    @objc_method
    def textViewDidEndEditing_(self, text_view):
        self.placeholder_label.setHidden_(len(text_view.text) > 0)


class MultilineTextInput(Widget):
    def create(self):
        self.native = TogaMultilineTextView.alloc().init()
        self.native.interface = self.interface
        self.native.impl = self
        self.native.delegate = self.native

        # Placeholder isn't natively supported, so we create our
        # own
        self.placeholder_label = UILabel.alloc().init()
        self.placeholder_label.translatesAutoresizingMaskIntoConstraints = False
        self.placeholder_label.font = self.native.font
        self.placeholder_label.alpha = 0.5
        self.native.addSubview_(self.placeholder_label)
        self.constrain_placeholder_label()

        # Delegate needs to update the placeholder depending on
        # input, so we give it just that to avoid a retain cycle
        self.native.placeholder_label = self.placeholder_label

        self.add_constraints()

    def constrain_placeholder_label(self):
        leading_constraint = \
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.placeholder_label,
                NSLayoutAttributeLeading,
                NSLayoutRelationEqual,
                self.native,
                NSLayoutAttributeLeading,
                1.0,
                4.0
            )
        trailing_constraint = \
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.placeholder_label,
                NSLayoutAttributeTrailing,
                NSLayoutRelationEqual,
                self.native,
                NSLayoutAttributeTrailing,
                1.0,
                0
            )
        top_constraint = \
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.placeholder_label,
                NSLayoutAttributeTop,
                NSLayoutRelationEqual,
                self.native,
                NSLayoutAttributeTop,
                1.0,
                8.0
            )
        bottom_constraint = \
            NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.placeholder_label,
                NSLayoutAttributeBottom,
                NSLayoutRelationEqual,
                self.native,
                NSLayoutAttributeBottom,
                1.0,
                0
            )
        self.native.addConstraints_([
            leading_constraint,
            trailing_constraint,
            top_constraint,
            bottom_constraint
        ])

    def set_placeholder(self, value):
        self.placeholder_label.text = value

    def set_readonly(self, value):
        self.native.editable = value

    def set_value(self, value):
        self.native.text = value
        self.placeholder_label.setHidden_(len(self.native.text) > 0)

    def get_value(self):
        return self.native.text

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)

    def set_font(self, font):
        if font:
            native_font = font.bind(self.interface.factory).native
            self.native.font = native_font
            self.placeholder_label.font = native_font

    def set_on_change(self, handler):
        self.interface.factory.not_implemented('MultilineTextInput.set_on_change()')
