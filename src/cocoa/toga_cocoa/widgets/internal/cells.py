from toga_cocoa.libs import (
    NSAffineTransform,
    NSBezierPath,
    NSColor,
    NSCompositingOperationSourceOver,
    NSFont,
    NSFontAttributeName,
    NSForegroundColorAttributeName,
    NSGraphicsContext,
    NSImageInterpolationHigh,
    NSImageView,
    NSMutableDictionary,
    NSPoint,
    NSRect,
    NSSize,
    NSTableCellView,
    NSTextField,
    NSTextFieldCell,
    NSLayoutAttributeLeft,
    NSLayoutAttributeRight,
    NSLayoutAttributeCenterY,
    NSLayoutAttributeWidth,
    NSLayoutAttributeNotAnAttribute,
    NSLayoutConstraint,
    NSLayoutRelationEqual,
    NSLineBreakMode,
    NSButton,
    NSSwitchButton,
    at,
    objc_method,
)


class TogaIconTextView(NSTableCellView):

    @objc_method
    def setup(self):
        self.imageView = NSImageView.alloc().init()
        self.checkbox = NSButton.alloc().init()
        self.textField = NSTextField.alloc().init()

        # this will retain image_view and text_field without needing to keep
        # a Python reference
        self.addSubview(self.imageView)
        self.addSubview(self.checkbox)
        self.addSubview(self.textField)

        self.checkbox.setButtonType(NSSwitchButton)

        self.textField.cell.lineBreakMode = NSLineBreakMode.byTruncatingTail
        self.textField.bordered = False
        self.textField.drawsBackground = False

        self.imageView.translatesAutoresizingMaskIntoConstraints = False
        self.checkbox.translatesAutoresizingMaskIntoConstraints = False
        self.textField.translatesAutoresizingMaskIntoConstraints = False

        # center icon vertically in cell
        self.iv_vertical_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # NOQA:E501
            self.imageView, NSLayoutAttributeCenterY,
            NSLayoutRelationEqual,
            self, NSLayoutAttributeCenterY,
            1, 0
            )
        # align left edge of icon with left edge of cell
        self.iv_left_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # NOQA:E501
            self.imageView, NSLayoutAttributeLeft,
            NSLayoutRelationEqual,
            self, NSLayoutAttributeLeft,
            1, 0
        )
        # set fixed width of icon
        self.iv_width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # NOQA:E501
            self.imageView, NSLayoutAttributeWidth,
            NSLayoutRelationEqual,
            None, NSLayoutAttributeNotAnAttribute,
            1, 16
        )
        # center checkbox vertically in cell
        self.cb_vertical_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # NOQA:E501
            self.checkbox, NSLayoutAttributeCenterY,
            NSLayoutRelationEqual,
            self, NSLayoutAttributeCenterY,
            1, 0
            )
        # align left edge of checkbox with right edge of icon
        self.cb_left_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # NOQA:E501
            self.checkbox, NSLayoutAttributeLeft,
            NSLayoutRelationEqual,
            self.imageView, NSLayoutAttributeRight,
            1, 5
        )
        # set fixed width of checkbox
        self.cb_width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # NOQA:E501
            self.checkbox, NSLayoutAttributeWidth,
            NSLayoutRelationEqual,
            None, NSLayoutAttributeNotAnAttribute,
            1, 16
        )
        # align text vertically in cell
        self.tv_vertical_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # NOQA:E501
            self.textField, NSLayoutAttributeCenterY,
            NSLayoutRelationEqual,
            self, NSLayoutAttributeCenterY,
            1, 0,
        )
        # align left edge of text with right edge of checkbox
        self.tv_left_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # NOQA:E501
            self.textField, NSLayoutAttributeLeft,
            NSLayoutRelationEqual,
            self.checkbox, NSLayoutAttributeRight,
            1, 5  # 5 pixels padding between checkbox and text
        )
        # align right edge of text with right edge of cell
        self.tv_right_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # NOQA:E501
            self.textField, NSLayoutAttributeRight,
            NSLayoutRelationEqual,
            self, NSLayoutAttributeRight,
            1, -5
        )

        self.addConstraint(self.iv_vertical_constraint)
        self.addConstraint(self.iv_left_constraint)
        self.addConstraint(self.iv_width_constraint)
        self.addConstraint(self.cb_vertical_constraint)
        self.addConstraint(self.cb_left_constraint)
        self.addConstraint(self.cb_width_constraint)
        self.addConstraint(self.tv_vertical_constraint)
        self.addConstraint(self.tv_left_constraint)
        self.addConstraint(self.tv_right_constraint)

    @objc_method
    def setImage_(self, image):

        if not self.imageView:
            self.setup()

        if image:
            self.imageView.image = image
            self.iv_width_constraint.constant = 16
            self.cb_left_constraint.constant = 5
        else:
            self.imageView.image = None
            self.iv_width_constraint.constant = 0
            self.cb_left_constraint.constant = 0

    @objc_method
    def setCheckState_(self, value):

        if not self.imageView:
            self.setup()

        if isinstance(value, int):
            self.cb_width_constraint.constant = 16
            self.tv_left_constraint.constant = 5
            self.checkbox.state = value

        if value is None:
            self.cb_width_constraint.constant = 0
            self.tv_left_constraint.constant = 0

    @objc_method
    def setText_(self, text):

        if not self.imageView:
            self.setup()

        self.textField.stringValue = text or ""


# A TogaDetailedCell contains:
# * an icon
# * a main label
# * a secondary label
class TogaDetailedCell(NSTextFieldCell):
    @objc_method
    def drawInteriorWithFrame_inView_(self, cellFrame: NSRect, view) -> None:
        # The data to display.
        icon = self.objectValue.attrs['icon']
        title = self.objectValue.attrs['title']
        subtitle = self.objectValue.attrs['subtitle']

        if icon and icon.native:
            NSGraphicsContext.currentContext.saveGraphicsState()
            yOffset = cellFrame.origin.y
            if view.isFlipped:
                xform = NSAffineTransform.transform()
                xform.translateXBy(4, yBy=cellFrame.size.height)
                xform.scaleXBy(1.0, yBy=-1.0)
                xform.concat()
                yOffset = 0.5 - cellFrame.origin.y

            interpolation = NSGraphicsContext.currentContext.imageInterpolation
            NSGraphicsContext.currentContext.imageInterpolation = NSImageInterpolationHigh

            icon.native.drawInRect(
                NSRect(NSPoint(cellFrame.origin.x, yOffset + 4), NSSize(40.0, 40.0)),
                fromRect=NSRect(NSPoint(0, 0), NSSize(icon.native.size.width, icon.native.size.height)),
                operation=NSCompositingOperationSourceOver,
                fraction=1.0
            )

            NSGraphicsContext.currentContext.imageInterpolation = interpolation
            NSGraphicsContext.currentContext.restoreGraphicsState()
        else:
            path = NSBezierPath.bezierPathWithRect(
                NSRect(NSPoint(cellFrame.origin.x, cellFrame.origin.y + 4), NSSize(40.0, 40.0))
            )
            NSColor.grayColor.set()
            path.fill()

        if title:
            # Find the right color for the text
            if self.isHighlighted():
                primaryColor = NSColor.alternateSelectedControlTextColor
            else:
                if False:
                    primaryColor = NSColor.disabledControlTextColor
                else:
                    primaryColor = NSColor.textColor

            textAttributes = NSMutableDictionary.alloc().init()
            textAttributes[NSForegroundColorAttributeName] = primaryColor
            textAttributes[NSFontAttributeName] = NSFont.systemFontOfSize(15)

            at(title).drawAtPoint(
                NSPoint(cellFrame.origin.x + 48, cellFrame.origin.y + 4),
                withAttributes=textAttributes
            )

        if subtitle:
            # Find the right color for the text
            if self.isHighlighted():
                primaryColor = NSColor.alternateSelectedControlTextColor
            else:
                if False:
                    primaryColor = NSColor.disabledControlTextColor
                else:
                    primaryColor = NSColor.textColor

            textAttributes = NSMutableDictionary.alloc().init()
            textAttributes[NSForegroundColorAttributeName] = primaryColor
            textAttributes[NSFontAttributeName] = NSFont.systemFontOfSize(13)

            at(subtitle).drawAtPoint(
                NSPoint(cellFrame.origin.x + 48, cellFrame.origin.y + 24),
                withAttributes=textAttributes
            )
