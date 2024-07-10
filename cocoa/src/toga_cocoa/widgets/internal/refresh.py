from ctypes import c_void_p

from rubicon.objc import (
    ObjCInstance,
    objc_method,
    objc_property,
    send_super,
)

from toga_cocoa.libs import (
    NSBezelBorder,
    NSClipView,
    NSEventPhaseBegan,
    NSLayoutAttributeCenterX,
    NSLayoutAttributeCenterY,
    NSLayoutAttributeHeight,
    NSLayoutAttributeNotAnAttribute,
    NSLayoutAttributeTop,
    NSLayoutAttributeWidth,
    NSLayoutConstraint,
    NSLayoutRelationEqual,
    NSMakePoint,
    NSMakeRect,
    NSPoint,
    NSProgressIndicator,
    NSProgressIndicatorSpinningStyle,
    NSRect,
    NSScrollElasticityAllowed,
    NSScrollView,
    NSView,
)

#########################################################################################
# This is broadly derived from Alex Zielenski's ScrollToRefresh implementation:
# https://github.com/alexzielenski/ScrollToRefresh/blob/master/ScrollToRefresh/src/EQSTRScrollView.m
# =======================================================================================
# ScrollToRefresh
#
# Copyright (C) 2011 by Alex Zielenski.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# =======================================================================================
#
# HOW THIS WORKS
#
# RefreshableScrollView is a subclass of NSScrollView. When it is created, it is
# provided a document (usually a List View); the RefreshableScrollView has a custom
# clipView that accommodates an extra widget which can display the "currently loading"
# spinner. When the scroll view is reloading, the clipView alters its bounds to include
# the extra space for the refresh_view header; when the reload finishes, an artificial
# scroll event is generated that forces the clipView to re-evaluate its bounds, removing
# the refresh_view.
#
# During a scroll action, a ``scrollWheel:`` event is generated. During normal in-bounds
# scrolling, the y origin of the content area will always be non-negative. If you're
# near the end of the scroll area and bounce against the end, you won't generate an
# event scroll event with a negative y origin. However, if you're already at the end of
# the scroll area, and you pull past the limit, you'll generate a scroll event with a
# negative origin. The scrollingDeltaY associated with that event indicates how hard you
# pulled past the limit; as long the size of the pull exceeds a threshold (this allows
# us to ignoring small/accidental scrolls), a reload event is generated. The bounds of
# the content area are forcibly extended to include the refresh view.
#
# All of this is also gated by the refreshEnabled flag; when refresh is disabled, it
# also makes the refresh widget invisible so that it can't be seen in a bounce scroll.
#########################################################################################

# The height of the refresh header; also the minimum pull height to trigger a refresh.
HEADER_HEIGHT = 45.0


class RefreshableClipView(NSClipView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def constrainScrollPoint_(self, proposedNewOrigin: NSPoint) -> NSPoint:
        constrained = send_super(
            __class__,
            self,
            "constrainScrollPoint:",
            proposedNewOrigin,
            restype=NSPoint,
            argtypes=[NSPoint],
        )

        # FIXME: This has been marked no-cover so that ARM64 testing can be enabled;
        # ARM64 CI can only run on Sonoma, and it looks like Sonoma has turned off
        # scroll elasticity by default, which prevents pull-to-refresh from working.
        # See Toga#2412 for details. If that ticket is closed, it should be possible
        # to remove this this no-cover.
        if self.superview and self.superview.is_refreshing:  # pragma: no cover
            return NSMakePoint(
                constrained.x,
                max(
                    proposedNewOrigin.y, -self.superview.refresh_view.frame.size.height
                ),
            )

        return constrained

    @objc_method
    def documentRect(self) -> NSRect:
        rect = send_super(__class__, self, "documentRect", restype=NSRect, argtypes=[])

        if self.superview and self.superview.is_refreshing:
            return NSMakeRect(
                rect.origin.x,
                rect.origin.y - self.superview.refresh_view.frame.size.height,
                rect.size.width,
                rect.size.height + self.superview.refresh_view.frame.size.height,
            )
        return rect


class RefreshableScrollView(NSScrollView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def initWithDocument_(self, documentView):
        self = ObjCInstance(send_super(__class__, self, "init"))
        self.hasVerticalScroller = True
        self.verticalScrollElasticity = NSScrollElasticityAllowed
        self.hasHorizontalScroller = False
        self.autohidesScrollers = False
        self.borderType = NSBezelBorder

        # Set local refresh-controlling properties
        self.event_ended = False
        self.is_refreshing = False

        # Create the clipview that contains the document and refresh view.
        superClipView = ObjCInstance(send_super(__class__, self, "contentView"))
        clipView = RefreshableClipView.alloc().initWithFrame(superClipView.frame)

        clipView.documentView = documentView
        clipView.copiesOnScroll = False
        clipView.drawsBackground = False

        self.setContentView(clipView)

        self.contentView.postsFrameChangedNotifications = True
        self.contentView.postsBoundsChangedNotifications = True

        # Create view to hold the refresh widgets
        self.refresh_view = NSView.alloc().init()
        self.refresh_view.translatesAutoresizingMaskIntoConstraints = False

        # Create spinner
        self.refresh_indicator = NSProgressIndicator.alloc().init()
        self.refresh_indicator.style = NSProgressIndicatorSpinningStyle
        self.refresh_indicator.translatesAutoresizingMaskIntoConstraints = False
        self.refresh_indicator.displayedWhenStopped = True
        self.refresh_indicator.usesThreadedAnimation = True
        self.refresh_indicator.indeterminate = True
        self.refresh_indicator.bezeled = False
        self.refresh_indicator.sizeToFit()

        # Hide the refresh indicator by default; this will be made visible when refresh
        # is explicitly enabled.
        self.refresh_indicator.setHidden(True)

        # Center the spinner in the header
        self.refresh_indicator.setFrame(
            NSMakeRect(
                self.refresh_view.bounds.size.width / 2
                - self.refresh_indicator.frame.size.width / 2,
                self.refresh_view.bounds.size.height / 2
                - self.refresh_indicator.frame.size.height / 2,
                self.refresh_indicator.frame.size.width,
                self.refresh_indicator.frame.size.height,
            )
        )

        # Put everything in place
        self.refresh_view.addSubview(self.refresh_indicator)
        self.contentView.addSubview(self.refresh_view)

        # set layout constraints
        indicatorHCenter = NSLayoutConstraint.constraintWithItem(
            self.refresh_indicator,
            attribute__1=NSLayoutAttributeCenterX,
            relatedBy=NSLayoutRelationEqual,
            toItem=self.refresh_view,
            attribute__2=NSLayoutAttributeCenterX,
            multiplier=1.0,
            constant=0,
        )
        self.refresh_view.addConstraint(indicatorHCenter)

        indicatorVCenter = NSLayoutConstraint.constraintWithItem(
            self.refresh_indicator,
            attribute__1=NSLayoutAttributeCenterY,
            relatedBy=NSLayoutRelationEqual,
            toItem=self.refresh_view,
            attribute__2=NSLayoutAttributeCenterY,
            multiplier=1.0,
            constant=0,
        )
        self.refresh_view.addConstraint(indicatorVCenter)

        refreshWidth = NSLayoutConstraint.constraintWithItem(
            self.refresh_view,
            attribute__1=NSLayoutAttributeWidth,
            relatedBy=NSLayoutRelationEqual,
            toItem=self.contentView,
            attribute__2=NSLayoutAttributeWidth,
            multiplier=1.0,
            constant=0,
        )
        self.contentView.addConstraint(refreshWidth)

        refreshHeight = NSLayoutConstraint.constraintWithItem(
            self.refresh_view,
            attribute__1=NSLayoutAttributeHeight,
            relatedBy=NSLayoutRelationEqual,
            toItem=None,
            attribute__2=NSLayoutAttributeNotAnAttribute,
            multiplier=1.0,
            constant=HEADER_HEIGHT,
        )
        self.contentView.addConstraint(refreshHeight)

        refreshHeight = NSLayoutConstraint.constraintWithItem(
            self.refresh_view,
            attribute__1=NSLayoutAttributeTop,
            relatedBy=NSLayoutRelationEqual,
            toItem=self.contentView,
            attribute__2=NSLayoutAttributeTop,
            multiplier=1.0,
            constant=-HEADER_HEIGHT,
        )
        self.contentView.addConstraint(refreshHeight)

        # Scroll to top
        contentRect = self.contentView.documentView.frame
        self.contentView.scrollToPoint(NSMakePoint(contentRect.origin.x, 0))
        self.reflectScrolledClipView(self.contentView)

        return self

    @objc_method
    def setRefreshEnabled(self, enabled: bool):
        self.refresh_enabled = enabled
        self.refresh_indicator.setHidden(not enabled)

    ######################################################################
    # Detecting scroll
    ######################################################################
    @objc_method
    def scrollWheel_(self, event) -> None:
        if (
            self.refresh_enabled
            and event.momentumPhase == NSEventPhaseBegan
            and event.scrollingDeltaY > HEADER_HEIGHT
            and self.contentView.bounds.origin.y < 0
        ):
            self.is_refreshing = True
            # Extend the content view area to ensure the refresh view is visible,
            # start the loading animation, and trigger the user's refresh handler.
            self.contentView.scrollToPoint(
                NSMakePoint(self.contentView.bounds.origin.x, -HEADER_HEIGHT)
            )
            self.refresh_indicator.startAnimation(self)
            self.interface.on_refresh()

        send_super(__class__, self, "scrollWheel:", event, argtypes=[c_void_p])

    @objc_method
    def finishedLoading(self):
        """Invoke to mark the end of a reload, stopping and hiding the reload
        spinner."""
        self.is_refreshing = False
        self.refresh_indicator.stopAnimation(self)
        self.documentView.reloadData()

        # Scroll back to top, hiding the refresh window from view.
        contentRect = self.contentView.documentView.frame
        self.contentView.scrollToPoint(NSMakePoint(contentRect.origin.x, 0))
        self.reflectScrolledClipView(self.contentView)
