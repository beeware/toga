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
    NSLayoutAttributeCenterY,
    NSLayoutAttributeLeft,
    NSLayoutAttributeNotAnAttribute,
    NSLayoutAttributeRight,
    NSLayoutAttributeWidth,
    NSLayoutConstraint,
    NSLayoutRelationEqual,
    NSLineBreakMode,
    NSMutableDictionary,
    NSPoint,
    NSRect,
    NSSize,
    NSTableCellView,
    NSTextField,
    NSTextFieldCell,
    at,
    objc_method,
)


class TogaIconView(NSTableCellView):
    @objc_method
    def setup(self):
        image_view = NSImageView.alloc().init()
        text_field = NSTextField.alloc().init()

        # this will retain image_view and text_field without needing to keep
        # a Python reference
        self.addSubview(image_view)
        self.addSubview(text_field)

        self.imageView = image_view
        self.textField = text_field

        self.textField.cell.lineBreakMode = NSLineBreakMode.byTruncatingTail
        self.textField.bordered = False
        self.textField.drawsBackground = False

        self.imageView.translatesAutoresizingMaskIntoConstraints = False
        self.textField.translatesAutoresizingMaskIntoConstraints = False

        # center icon vertically in cell
        self.iv_vertical_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # NOQA:E501
            self.imageView,
            NSLayoutAttributeCenterY,
            NSLayoutRelationEqual,
            self,
            NSLayoutAttributeCenterY,
            1,
            0,
        )
        # align left edge of icon with left edge of cell
        self.iv_left_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # NOQA:E501
            self.imageView,
            NSLayoutAttributeLeft,
            NSLayoutRelationEqual,
            self,
            NSLayoutAttributeLeft,
            1,
            0,
        )
        # set fixed width of icon
        self.iv_width_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # NOQA:E501
            self.imageView,
            NSLayoutAttributeWidth,
            NSLayoutRelationEqual,
            None,
            NSLayoutAttributeNotAnAttribute,
            1,
            16,
        )
        # align text vertically in cell
        self.tv_vertical_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # NOQA:E501
            self.textField,
            NSLayoutAttributeCenterY,
            NSLayoutRelationEqual,
            self,
            NSLayoutAttributeCenterY,
            1,
            0,
        )
        # align left edge of text with right edge of icon
        self.tv_left_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # NOQA:E501
            self.textField,
            NSLayoutAttributeLeft,
            NSLayoutRelationEqual,
            self.imageView,
            NSLayoutAttributeRight,
            1,
            5,  # 5 pixels padding between icon and text
        )
        # align right edge of text with right edge of cell
        self.tv_right_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(  # NOQA:E501
            self.textField,
            NSLayoutAttributeRight,
            NSLayoutRelationEqual,
            self,
            NSLayoutAttributeRight,
            1,
            -5,
        )

        self.addConstraint(self.iv_vertical_constraint)
        self.addConstraint(self.iv_left_constraint)
        self.addConstraint(self.iv_width_constraint)
        self.addConstraint(self.tv_vertical_constraint)
        self.addConstraint(self.tv_left_constraint)
        self.addConstraint(self.tv_right_constraint)

    @objc_method
    def setImage_(self, image):

        if not self.imageView:
            self.setup()

        if image:
            self.imageView.image = image
            # set icon width to 16
            self.iv_width_constraint.constant = 16
            # add padding between icon and text
            self.tv_left_constraint.constant = 5
        else:
            self.imageView.image = None
            # set icon width to 0
            self.iv_width_constraint.constant = 0
            # remove padding between icon and text
            self.tv_left_constraint.constant = 0

    @objc_method
    def setText_(self, text):

        if not self.imageView:
            self.setup()

        self.textField.stringValue = text


# A TogaDetailedCell contains:
# * an icon
# * a main label
# * a secondary label
class TogaDetailedCell(NSTextFieldCell):
    @objc_method
    def drawInteriorWithFrame_inView_(self, cellFrame: NSRect, view) -> None:
        # The data to display.
        icon = self.objectValue.attrs["icon"]
        title = self.objectValue.attrs["title"]
        subtitle = self.objectValue.attrs["subtitle"]

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
            NSGraphicsContext.currentContext.imageInterpolation = (
                NSImageInterpolationHigh
            )

            icon.native.drawInRect(
                NSRect(NSPoint(cellFrame.origin.x, yOffset + 4), NSSize(40.0, 40.0)),
                fromRect=NSRect(
                    NSPoint(0, 0),
                    NSSize(icon.native.size.width, icon.native.size.height),
                ),
                operation=NSCompositingOperationSourceOver,
                fraction=1.0,
            )

            NSGraphicsContext.currentContext.imageInterpolation = interpolation
            NSGraphicsContext.currentContext.restoreGraphicsState()
        else:
            path = NSBezierPath.bezierPathWithRect(
                NSRect(
                    NSPoint(cellFrame.origin.x, cellFrame.origin.y + 4),
                    NSSize(40.0, 40.0),
                )
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
                withAttributes=textAttributes,
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
                withAttributes=textAttributes,
            )
