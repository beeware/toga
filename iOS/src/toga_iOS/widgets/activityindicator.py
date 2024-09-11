from rubicon.objc import CGSize

from toga_iOS.libs import UIActivityIndicatorView, UIView
from toga_iOS.widgets.base import Widget


class ActivityIndicator(Widget):
    def create(self):
        """Implements the ActivityIndicator widget for iOS

        Implementation note:
        ===================

        The UIActivityIndicatorView is added to a parent UIView because
        there is an issue with the UIActivityIndicatorView's `hidesWhenStopped`
        behavior - if it is not part of a parent UIView, the indicator
        is immediately visible even when not animating, even when
        `hidesWhenStopped` is set to `True`, but it works as expected when
        it is added as a subview to a parent UIView.
        """

        self._activity_indicator = UIActivityIndicatorView.new()
        self._activity_indicator.hidesWhenStopped = True
        self._activity_indicator.translatesAutoresizingMaskIntoConstraints = False

        self.native = UIView.new()
        self.native.addSubview(self._activity_indicator)
        self.native.translatesAutoresizingMaskIntoConstraints = False
        self.native.sizeToFit()

        self.add_constraints()

    def is_running(self):
        return self._activity_indicator.isAnimating()

    def start(self):
        self._activity_indicator.startAnimating()

    def stop(self):
        self._activity_indicator.stopAnimating()

    def rehint(self):
        fitting_size = self._activity_indicator.systemLayoutSizeFittingSize(
            CGSize(0, 0)
        )
        self.interface.intrinsic.width = fitting_size.width
        self.interface.intrinsic.height = fitting_size.height
