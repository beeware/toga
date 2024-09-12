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

    def is_running(self):
        return self.native.isAnimating()

    def start(self):
        self.native.startAnimating()

    def stop(self):
        self.native.stopAnimating()

    def rehint(self):
        fitting_size = self.native.systemLayoutSizeFittingSize(CGSize(0, 0))
        self.interface.intrinsic.width = fitting_size.width
        self.interface.intrinsic.height = fitting_size.height
