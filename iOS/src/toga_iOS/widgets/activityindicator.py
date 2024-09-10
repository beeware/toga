from rubicon.objc import CGSize

from toga_iOS.libs import UIActivityIndicatorView, UIView
from toga_iOS.widgets.base import Widget


class ActivityIndicator(Widget):
    def create(self):
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
