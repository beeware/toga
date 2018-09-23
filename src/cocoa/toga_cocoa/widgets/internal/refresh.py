from rubicon.objc import *

from toga_cocoa.libs import *

HEADER_HEIGHT = 45.0


class RefreshableClipView(NSClipView):
    @objc_method
    def constrainScrollPoint_(self, proposedNewOrigin: NSPoint) -> NSPoint:
        constrained = send_super(
            __class__, self, 'constrainScrollPoint:', proposedNewOrigin,
            restype=NSPoint, argtypes=[NSPoint]
        )

        if self.superview and self.superview.refreshTriggered:
            return NSMakePoint(
                constrained.x,
                max(proposedNewOrigin.y, -self.superview.refreshView.frame.size.height)
            )

        return constrained

    @objc_method
    def isFlipped(self):
        return True

    @objc_method
    def documentRect(self) -> NSRect:
        rect = send_super(__class__, self, 'documentRect', restype=NSRect, argtypes=[])

        if self.superview and self.superview.refreshTriggered:
            return NSMakeRect(
                rect.origin.x, rect.origin.y - self.superview.refreshView.frame.size.height,
                rect.size.width, rect.size.height + self.superview.refreshView.frame.size.height
            )
        return rect


class RefreshableScrollView(NSScrollView):
    # Create Header View
    @objc_method
    def viewDidMoveToWindow(self) -> None:
        self.refreshTriggered = False
        self.isRefreshing = False
        self.refreshView = None
        self.refreshIndicator = None
        self.createRefreshView()

    @objc_method
    def createContentView(self):
        superClipView = ObjCInstance(send_super(__class__, self, 'contentView'))
        if not isinstance(superClipView, RefreshableClipView):
            # create new clipview
            documentView = superClipView.documentView
            clipView = RefreshableClipView.alloc().initWithFrame(superClipView.frame)

            clipView.documentView = documentView
            clipView.copiesOnScroll = False
            clipView.drawsBackground = False

            self.setContentView(clipView)
            superClipView = ObjCInstance(send_super(__class__, self, 'contentView'))

        return superClipView

    @objc_method
    def createRefreshView(self) -> None:
        # delete old stuff if any
        if self.refreshView:
            self.refreshView.removeFromSuperview()
            self.refreshView.release()
            self.refreshView = None

        self.verticalScrollElasticity = NSScrollElasticityAllowed

        # create new content view
        self.createContentView()

        self.contentView.postsFrameChangedNotifications = True
        self.contentView.postsBoundsChangedNotifications = True

        NSNotificationCenter.defaultCenter.addObserver(
            self,
            selector=SEL('viewBoundsChanged:'),
            name=NSViewBoundsDidChangeNotification,
            object=self.contentView,
        )

        # Create view to hold the refresh widgets refreshview
        contentRect = self.contentView.documentView.frame
        self.refreshView = NSView.alloc().init()
        self.refreshView.translatesAutoresizingMaskIntoConstraints = False

        # Create spinner
        self.refreshIndicator = NSProgressIndicator.alloc().init()
        self.refreshIndicator.style = NSProgressIndicatorSpinningStyle;
        self.refreshIndicator.translatesAutoresizingMaskIntoConstraints = False
        self.refreshIndicator.displayedWhenStopped = True
        self.refreshIndicator.usesThreadedAnimation = True
        self.refreshIndicator.indeterminate = True
        self.refreshIndicator.bezeled = False
        self.refreshIndicator.sizeToFit()

        # Center the spinner in the header
        self.refreshIndicator.setFrame(
            NSMakeRect(
                self.refreshView.bounds.size.width / 2 - self.refreshIndicator.frame.size.width / 2,
                self.refreshView.bounds.size.height / 2 - self.refreshIndicator.frame.size.height / 2,
                self.refreshIndicator.frame.size.width,
                self.refreshIndicator.frame.size.height
            )
        )

        # Put everything in place
        self.refreshView.addSubview(self.refreshIndicator)
        # self.refreshView.addSubview(self.refreshArrow)
        self.contentView.addSubview(self.refreshView)

        # set layout constraints
        indicatorHCenter = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.refreshIndicator, NSLayoutAttributeCenterX,
            NSLayoutRelationEqual,
            self.refreshView, NSLayoutAttributeCenterX,
            1.0, 0,
        )
        self.refreshView.addConstraint(indicatorHCenter)

        indicatorVCenter = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.refreshIndicator, NSLayoutAttributeCenterY,
            NSLayoutRelationEqual,
            self.refreshView, NSLayoutAttributeCenterY,
            1.0, 0,
        )
        self.refreshView.addConstraint(indicatorVCenter)

        refreshWidth = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.refreshView, NSLayoutAttributeWidth,
            NSLayoutRelationEqual,
            self.contentView, NSLayoutAttributeWidth,
            1.0, 0,
        )
        self.contentView.addConstraint(refreshWidth)

        refreshHeight = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.refreshView, NSLayoutAttributeHeight,
            NSLayoutRelationEqual,
            None, NSLayoutAttributeNotAnAttribute,
            1.0, HEADER_HEIGHT,
        )
        self.contentView.addConstraint(refreshHeight)

        refreshHeight = NSLayoutConstraint.constraintWithItem_attribute_relatedBy_toItem_attribute_multiplier_constant_(
            self.refreshView, NSLayoutAttributeTop,
            NSLayoutRelationEqual,
            self.contentView, NSLayoutAttributeTop,
            1.0, -HEADER_HEIGHT,
        )
        self.contentView.addConstraint(refreshHeight)

        # Scroll to top
        self.contentView.scrollToPoint(NSMakePoint(contentRect.origin.x, 0));
        self.reflectScrolledClipView(self.contentView)

    # Detecting scroll
    @objc_method
    def scrollWheel_(self, event) -> None:
        if event.phase == NSEventPhaseEnded:
            if self.refreshTriggered and not self.isRefreshing:
                self.reload()

        send_super(__class__, self, 'scrollWheel:', event)

    @objc_method
    def viewBoundsChanged_(self, note) -> None:
        if self.isRefreshing:
            return

        if self.contentView.bounds.origin.y <= -self.refreshView.frame.size.height:
            self.refreshTriggered = True

    # Reload
    @objc_method
    def reload(self) -> None:
        """Start a reload, starting the reload spinner"""
        self.isRefreshing = True
        self.refreshIndicator.startAnimation(self)
        self.interface.on_refresh(self.interface)

    @objc_method
    def finishedLoading(self):
        """Invoke to mark the end of a reload, stopping and hiding the reload spinner"""
        self.isRefreshing = False
        self.refreshTriggered = False
        self.refreshIndicator.stopAnimation(self)
        self.detailedlist.reloadData()

        # Force a scroll event to make the scroll hide the reload
        cgEvent = core_graphics.CGEventCreateScrollWheelEvent(None, kCGScrollEventUnitLine, 2, 1, 0)
        scrollEvent = NSEvent.eventWithCGEvent(cgEvent)
        self.scrollWheel(scrollEvent)
