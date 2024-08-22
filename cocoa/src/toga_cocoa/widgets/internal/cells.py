from rubicon.objc import at, objc_method

from toga_cocoa.libs import (
    NSAffineTransform,
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
        self.iv_vertical_constraint = NSLayoutConstraint.constraintWithItem(
            self.imageView,
            attribute__1=NSLayoutAttributeCenterY,
            relatedBy=NSLayoutRelationEqual,
            toItem=self,
            attribute__2=NSLayoutAttributeCenterY,
            multiplier=1,
            constant=0,
        )
        # align left edge of icon with left edge of cell
        self.iv_left_constraint = NSLayoutConstraint.constraintWithItem(
            self.imageView,
            attribute__1=NSLayoutAttributeLeft,
            relatedBy=NSLayoutRelationEqual,
            toItem=self,
            attribute__2=NSLayoutAttributeLeft,
            multiplier=1,
            constant=0,
        )
        # set fixed width of icon
        self.iv_width_constraint = NSLayoutConstraint.constraintWithItem(
            self.imageView,
            attribute__1=NSLayoutAttributeWidth,
            relatedBy=NSLayoutRelationEqual,
            toItem=None,
            attribute__2=NSLayoutAttributeNotAnAttribute,
            multiplier=1,
            constant=6,
        )
        # align text vertically in cell
        self.tv_vertical_constraint = NSLayoutConstraint.constraintWithItem(
            self.textField,
            attribute__1=NSLayoutAttributeCenterY,
            relatedBy=NSLayoutRelationEqual,
            toItem=self,
            attribute__2=NSLayoutAttributeCenterY,
            multiplier=1,
            constant=0,
        )
        # align left edge of text with right edge of icon
        self.tv_left_constraint = NSLayoutConstraint.constraintWithItem(
            self.textField,
            attribute__1=NSLayoutAttributeLeft,
            relatedBy=NSLayoutRelationEqual,
            toItem=self.imageView,
            attribute__2=NSLayoutAttributeRight,
            multiplier=1,
            constant=5,  # 5 pixels padding between icon and text
        )
        # align right edge of text with right edge of cell
        self.tv_right_constraint = NSLayoutConstraint.constraintWithItem(
            self.textField,
            attribute__1=NSLayoutAttributeRight,
            relatedBy=NSLayoutRelationEqual,
            toItem=self,
            attribute__2=NSLayoutAttributeRight,
            multiplier=1,
            constant=-5,
        )

        self.addConstraint(self.iv_vertical_constraint)
        self.addConstraint(self.iv_left_constraint)
        self.addConstraint(self.iv_width_constraint)
        self.addConstraint(self.tv_vertical_constraint)
        self.addConstraint(self.tv_left_constraint)
        self.addConstraint(self.tv_right_constraint)

    @objc_method
    def setImage_(self, image):
        # This branch is here for future protection - but the image is *never* set
        # before the text, so it can't ever happen.
        if not self.imageView:  # pragma: no cover
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
# * a main "title" label
# * a secondary "subtitle" label
class TogaDetailedCell(NSTextFieldCell):
    @objc_method
    def drawInteriorWithFrame_inView_(self, cellFrame: NSRect, view) -> None:
        # The data to display.
        icon = self.objectValue.attrs["icon"]
        title = self.objectValue.attrs["title"]
        subtitle = self.objectValue.attrs["subtitle"]

        # If there's an icon, draw it.
        if icon:
            NSGraphicsContext.currentContext.saveGraphicsState()
            yOffset = cellFrame.origin.y

            # Coordinate system is always flipped
            xform = NSAffineTransform.transform()
            xform.translateXBy(4, yBy=cellFrame.size.height)
            xform.scaleXBy(1.0, yBy=-1.0)
            xform.concat()
            yOffset = 0.5 - cellFrame.origin.y

            interpolation = NSGraphicsContext.currentContext.imageInterpolation
            NSGraphicsContext.currentContext.imageInterpolation = (
                NSImageInterpolationHigh
            )

            icon.drawInRect(
                NSRect(NSPoint(cellFrame.origin.x, yOffset + 4), NSSize(40.0, 40.0)),
                fromRect=NSRect(
                    NSPoint(0, 0),
                    NSSize(icon.size.width, icon.size.height),
                ),
                operation=NSCompositingOperationSourceOver,
                fraction=1.0,
            )

            NSGraphicsContext.currentContext.imageInterpolation = interpolation
            NSGraphicsContext.currentContext.restoreGraphicsState()

        # Find the right color for the text
        if self.isHighlighted():
            primaryColor = NSColor.alternateSelectedControlTextColor
        else:
            primaryColor = NSColor.textColor

        # Draw the title
        textAttributes = NSMutableDictionary.alloc().init()
        textAttributes[NSForegroundColorAttributeName] = primaryColor
        textAttributes[NSFontAttributeName] = NSFont.systemFontOfSize(15)

        at(title).drawAtPoint(
            NSPoint(cellFrame.origin.x + 48, cellFrame.origin.y + 4),
            withAttributes=textAttributes,
        )

        # Draw the subtitle
        textAttributes = NSMutableDictionary.alloc().init()
        textAttributes[NSForegroundColorAttributeName] = primaryColor
        textAttributes[NSFontAttributeName] = NSFont.systemFontOfSize(13)

        at(subtitle).drawAtPoint(
            NSPoint(cellFrame.origin.x + 48, cellFrame.origin.y + 24),
            withAttributes=textAttributes,
        )
