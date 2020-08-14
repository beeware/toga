from toga_cocoa.libs import (
    CGRect,
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
    NSLayoutConstraint,
    NSLayoutRelationEqual,
    NSLineBreakMode,
    ObjCInstance,
    at,
    objc_method,
    send_super
)


class TogaIconView(NSTableCellView):

    @objc_method
    def initWithFrame_(self, frame: CGRect):
        self = ObjCInstance(send_super(__class__, self, 'initWithFrame:', frame))
        return self.setup()

    @objc_method
    def init(self):
        self = ObjCInstance(send_super(__class__, self, 'init'))
        return self.setup()

    @objc_method
    def setup(self):
        self.imageView = NSImageView.alloc().init()
        self.textField = NSTextField.alloc().init()

        self.textField.cell.lineBreakMode = NSLineBreakMode.byTruncatingTail
        self.textField.bordered = False
        self.textField.drawsBackground = False

        self.imageView.translatesAutoresizingMaskIntoConstraints = False
        self.textField.translatesAutoresizingMaskIntoConstraints = False

        self.addSubview(self.imageView)
        self.addSubview(self.textField)

        self.iv_vertical_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.imageView, NSLayoutAttributeCenterY, NSLayoutRelationEqual, self, NSLayoutAttributeCenterY, 1, 0
            )
        self.iv_left_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.imageView, NSLayoutAttributeLeft, NSLayoutRelationEqual, self, NSLayoutAttributeLeft, 1, 0
        )
        self.tv_vertical_constraint =NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.textField, NSLayoutAttributeCenterY, NSLayoutRelationEqual, self, NSLayoutAttributeCenterY, 1, 0
        )
        self.tv_left_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.textField, NSLayoutAttributeLeft, NSLayoutRelationEqual, self.imageView, NSLayoutAttributeRight, 1, 5
        )
        self.tv_right_constraint = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
                self.textField, NSLayoutAttributeRight, NSLayoutRelationEqual, self, NSLayoutAttributeRight, 1, -5
        )

        self.addConstraint(self.iv_vertical_constraint)
        self.addConstraint(self.iv_left_constraint)
        self.addConstraint(self.tv_vertical_constraint)
        self.addConstraint(self.tv_left_constraint)
        self.addConstraint(self.tv_right_constraint)

        return self

    @objc_method
    def setImage(self, image):
        if image:
            self.imageView.image = image.resizeTo(16)
            # add padding between icon and text
            self.tv_left_constraint.constant = 5
        else:
            self.imageView.image = None
            # remove padding between icon and text
            self.tv_left_constraint.constant = 0

    @objc_method
    def setText(self, text):
        self.textField.stringValue = text


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
