from rubicon.objc import objc_method

from toga_cocoa.libs import (
    NSFont,
    NSImageView,
    NSLayoutAttributeBottom,
    NSLayoutAttributeCenterY,
    NSLayoutAttributeLeft,
    NSLayoutAttributeNotAnAttribute,
    NSLayoutAttributeRight,
    NSLayoutAttributeTop,
    NSLayoutAttributeWidth,
    NSLayoutConstraint,
    NSLayoutRelationEqual,
    NSLineBreakMode,
    NSTableCellView,
    NSTextField,
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
        self.textField.allowsExpansionToolTips = True
        self.textField.editable = False

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


class TogaDetailedView(NSTableCellView):
    @objc_method
    def setup(self):
        self.imageView = NSImageView.alloc().init()

        self.titleField = NSTextField.alloc().init()
        self.subtitleField = NSTextField.alloc().init()

        for field in (self.titleField, self.subtitleField):
            field.editable = False
            field.bordered = False
            field.drawsBackground = False
            field.selectable = False

        self.titleField.font = NSFont.systemFontOfSize(15)
        self.subtitleField.font = NSFont.systemFontOfSize(13)

        self.titleField.cell.lineBreakMode = NSLineBreakMode.byTruncatingTail
        self.subtitleField.cell.lineBreakMode = NSLineBreakMode.byTruncatingTail

        self.addSubview(self.imageView)
        self.addSubview(self.titleField)
        self.addSubview(self.subtitleField)

        self.imageView.translatesAutoresizingMaskIntoConstraints = False
        self.titleField.translatesAutoresizingMaskIntoConstraints = False
        self.subtitleField.translatesAutoresizingMaskIntoConstraints = False

        self.padding_constraint = NSLayoutConstraint.constraintWithItem(
            self.titleField,
            attribute__1=NSLayoutAttributeLeft,
            relatedBy=NSLayoutRelationEqual,
            toItem=self.imageView,
            attribute__2=NSLayoutAttributeRight,
            multiplier=1,
            constant=4,
        )
        self.width_constraint = NSLayoutConstraint.constraintWithItem(
            self.imageView,
            attribute__1=NSLayoutAttributeRight,
            relatedBy=NSLayoutRelationEqual,
            toItem=self,
            attribute__2=NSLayoutAttributeLeft,
            multiplier=1,
            constant=40,
        )
        constraints = [
            # icon
            self.width_constraint,
            NSLayoutConstraint.constraintWithItem(
                self.imageView,
                attribute__1=NSLayoutAttributeLeft,
                relatedBy=NSLayoutRelationEqual,
                toItem=self,
                attribute__2=NSLayoutAttributeLeft,
                multiplier=1,
                constant=4,
            ),
            NSLayoutConstraint.constraintWithItem(
                self.imageView,
                attribute__1=NSLayoutAttributeCenterY,
                relatedBy=NSLayoutRelationEqual,
                toItem=self,
                attribute__2=NSLayoutAttributeCenterY,
                multiplier=1,
                constant=0,
            ),
            # title
            self.padding_constraint,
            NSLayoutConstraint.constraintWithItem(
                self.titleField,
                attribute__1=NSLayoutAttributeTop,
                relatedBy=NSLayoutRelationEqual,
                toItem=self,
                attribute__2=NSLayoutAttributeTop,
                multiplier=1,
                constant=4,
            ),
            NSLayoutConstraint.constraintWithItem(
                self.titleField,
                attribute__1=NSLayoutAttributeRight,
                relatedBy=NSLayoutRelationEqual,
                toItem=self,
                attribute__2=NSLayoutAttributeRight,
                multiplier=1,
                constant=-4,
            ),
            # subtitle
            NSLayoutConstraint.constraintWithItem(
                self.subtitleField,
                attribute__1=NSLayoutAttributeTop,
                relatedBy=NSLayoutRelationEqual,
                toItem=self.titleField,
                attribute__2=NSLayoutAttributeBottom,
                multiplier=1,
                constant=2,
            ),
            NSLayoutConstraint.constraintWithItem(
                self.subtitleField,
                attribute__1=NSLayoutAttributeLeft,
                relatedBy=NSLayoutRelationEqual,
                toItem=self.titleField,
                attribute__2=NSLayoutAttributeLeft,
                multiplier=1,
                constant=0,
            ),
            NSLayoutConstraint.constraintWithItem(
                self.subtitleField,
                attribute__1=NSLayoutAttributeRight,
                relatedBy=NSLayoutRelationEqual,
                toItem=self.titleField,
                attribute__2=NSLayoutAttributeRight,
                multiplier=1,
                constant=0,
            ),
        ]

        for constraint in constraints:
            self.addConstraint(constraint)

    @objc_method
    def setTitle(self, title):
        self.titleField.stringValue = title

    @objc_method
    def setSubtitle(self, subtitle):
        self.subtitleField.stringValue = subtitle

    @objc_method
    def setIcon(self, icon):
        if icon:
            self.imageView.image = icon
            self.width_constraint.constant = 40
            self.padding_constraint.constant = 4
        else:
            self.imageView.image = None
            self.width_constraint.constant = 0
            self.padding_constraint.constant = 0
