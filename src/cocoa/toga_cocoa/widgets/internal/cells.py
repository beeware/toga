
from toga_cocoa.libs import (
    ObjCInstance, objc_method, send_super,
    NSTableCellView, NSImageView, NSTextField, NSTextFieldCell,
    NSViewMaxYMargin, NSViewMinYMargin, NSMutableDictionary,
    NSGraphicsContext, NSAffineTransform, NSImageInterpolationHigh,
    NSCompositingOperationSourceOver, NSColor, NSBezierPath,
    NSForegroundColorAttributeName, NSFontAttributeName, NSFont,
    NSImageScaleProportionallyDown, NSImageAlignment,
    NSSize, NSPoint, NSRect, NSMakePoint, NSMakeRect, CGRect, at
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
        iv = NSImageView.alloc().initWithFrame(NSMakeRect(0, 0, 16, 16))
        tf = NSTextField.alloc().init()

        iv.autoresizingMask = NSViewMinYMargin | NSViewMaxYMargin
        iv.imageScaling = NSImageScaleProportionallyDown
        iv.imageAlignment = NSImageAlignment.Center

        tf.autoresizingMask = NSViewMinYMargin | NSViewMaxYMargin
        tf.bordered = False
        tf.drawsBackground = False

        self.imageView = iv
        self.textField = tf
        self.addSubview(iv)
        self.addSubview(tf)
        return self

    @objc_method
    def setImage(self, image):
        if image is self.imageView.image:
            # don't do anything if image did not change
            return

        if image:
            self.imageView.image = image
            self.imageView.frame = NSMakeRect(5, 0, 16, 16)
            self.textField.frameOrigin = NSMakePoint(25, 0)
        else:
            self.imageView.image = None
            self.imageView.frame = NSMakeRect(0, 0, 0, 0)
            self.textField.frameOrigin = NSMakePoint(0, 0)

    @objc_method
    def setText(self, text):
        if text != self.textField.stringValue:
            self.textField.stringValue = text
            self.textField.sizeToFit()


class TogaIconCell(NSTextFieldCell):

    @objc_method
    def drawWithFrame_inView_(self, cellFrame: NSRect, view) -> None:
        # The data to display.
        try:
            label = self.objectValue.attrs['label']
            icon = self.objectValue.attrs['icon']
        except AttributeError:
            # Value is a simple string.
            label = self.objectValue
            icon = None

        if icon and icon.native:
            offset = 28.5

            NSGraphicsContext.currentContext.saveGraphicsState()
            yOffset = cellFrame.origin.y
            if view.isFlipped:
                xform = NSAffineTransform.transform()
                xform.translateXBy(8, yBy=cellFrame.size.height)
                xform.scaleXBy(1.0, yBy=-1.0)
                xform.concat()
                yOffset = 0.5 - cellFrame.origin.y

            interpolation = NSGraphicsContext.currentContext.imageInterpolation
            NSGraphicsContext.currentContext.imageInterpolation = NSImageInterpolationHigh

            icon.native.drawInRect(
                NSRect(NSPoint(cellFrame.origin.x, yOffset), NSSize(16.0, 16.0)),
                fromRect=NSRect(NSPoint(0, 0), NSSize(icon.native.size.width, icon.native.size.height)),
                operation=NSCompositingOperationSourceOver,
                fraction=1.0
            )

            NSGraphicsContext.currentContext.imageInterpolation = interpolation
            NSGraphicsContext.currentContext.restoreGraphicsState()
        else:
            # No icon; just the text label
            offset = 5

        if label:
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

            at(label).drawInRect(cellFrame, withAttributes=textAttributes)


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
