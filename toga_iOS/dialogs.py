from rubicon.objc import *

from .libs import *
from .widgets.base import WidgetMixin


class TogaDialog(UIViewController):
    @objc_method
    def loadView(self) -> None:
        self.title = self.interface.title

        self.cancelButton = UIBarButtonItem.alloc().initWithBarButtonSystemItem_target_action_(
            UIBarButtonSystemItemCancel,
            self,
            get_selector('cancelClicked')
        )
        self.navigationController.navigationBar.topItem.leftBarButtonItem = self.cancelButton

        self.doneButton = UIBarButtonItem.alloc().initWithBarButtonSystemItem_target_action_(
            UIBarButtonSystemItemDone,
            self,
            get_selector('doneClicked')
        )
        self.navigationController.navigationBar.topItem.rightBarButtonItem = self.doneButton

        self.interface.content._update_layout(
            width=UIScreen.mainScreen().bounds.size.width,
            height=UIScreen.mainScreen().bounds.size.height,
            padding_top=12
        )

        self.view = self.interface.content._impl

    @objc_method
    def cancelClicked(self):
        self.dismissModalViewControllerAnimated_(True)
        if self.interface.on_cancel:
            self.interface.on_cancel(self.interface)

    @objc_method
    def doneClicked(self):
        self.dismissModalViewControllerAnimated_(True)
        if self.interface.on_accept:
            self.interface.on_accept(self.interface)


class Dialog:
    def __init__(self, title, content, on_accept=None, on_cancel=None):
        self.title = title
        self.content = content

        self.on_accept = on_accept
        self.on_cancel = on_cancel

        self.startup()

    def startup(self):
        self.content.startup()
        self._impl = TogaDialog.alloc().init()
        self._impl.interface = self
