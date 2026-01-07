from rubicon.objc import CGSize

from toga_iOS.libs import UIActivityIndicatorView
from toga_iOS.widgets.base import Widget


class ActivityIndicator(Widget):
    def create(self):
        self.native = UIActivityIndicatorView.new()
        self.native.hidesWhenStopped = True
        self.native.translatesAutoresizingMaskIntoConstraints = False
        self.native.sizeToFit()

        self.add_constraints()

    def set_hidden(self, hidden):
        self.native.setHidden((not self.is_running()) or hidden)
        self._hidden = hidden

    def is_running(self):
        return self.native.isAnimating()

    def start(self):
        self.native.startAnimating()
        # The above due to using hidesWhenStopped actually shows the
        # indicator even if hidden!  So we work around that by explicitly
        # correcting visibility after we start animation.
        self.native.setHidden(self._hidden)

    def stop(self):
        self.native.stopAnimating()
        # Even if hidden the above command hides it, so it's at most redundant
        # No other action needed here

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = fitting_size.width
        self.interface.intrinsic.height = fitting_size.height
