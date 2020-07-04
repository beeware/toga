from rubicon.objc import SEL, Block, objc_method
from rubicon.objc.runtime import objc_id

from toga_iOS.libs import (
    NSDate,
    NSRunLoop,
    UIAlertAction,
    UIAlertActionStyle,
    UIAlertController,
    UIAlertControllerStyle,
    UIBarButtonItem,
    UIBarButtonSystemItem,
    UIScreen,
    UIViewController
)


class TogaDialog(UIViewController):
    @objc_method
    def loadView(self) -> None:
        self.title = self.interface.title

        self.cancelButton = UIBarButtonItem.alloc().initWithBarButtonSystemItem_target_action_(
            UIBarButtonSystemItem.Cancel,
            self,
            SEL('cancelClicked')
        )
        self.navigationController.navigationBar.topItem.leftBarButtonItem = self.cancelButton

        self.doneButton = UIBarButtonItem.alloc().initWithBarButtonSystemItem_target_action_(
            UIBarButtonSystemItem.Done,
            SEL('doneClicked')
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

        self._create()

    def _create(self):
        self.content.startup()
        self._native = TogaDialog.alloc().init()
        self._native.interface = self


class TogaModalDialog:
    def __init__(self, title, message):
        self.native = UIAlertController.alertControllerWithTitle(
            title,
            message=message,
            preferredStyle=UIAlertControllerStyle.Alert
        )

        self.response = None

    def true_response(self, action: objc_id) -> None:
        self.response = True

    def false_response(self, action: objc_id) -> None:
        self.response = False

    def add_ok_button(self):
        self.native.addAction(
            UIAlertAction.actionWithTitle(
                "OK",
                style=UIAlertActionStyle.Default,
                handler=Block(self.true_response, None, objc_id)
            )
        )

    def add_cancel_button(self):
        self.native.addAction(
            UIAlertAction.actionWithTitle(
                "Cancel",
                style=UIAlertActionStyle.Cancel,
                handler=Block(self.false_response, None, objc_id)
            )
        )

    def runModal(self, window):
        window._impl.controller.presentViewController(
            self.native,
            animated=False,
            completion=None,
        )

        while self.response is None:
            NSRunLoop.currentRunLoop().runUntilDate(NSDate.alloc().init())

        return self.response


def info_dialog(window, title, message):
    dialog = TogaModalDialog(title=title, message=message)
    dialog.add_ok_button()
    return dialog.runModal(window)


def question_dialog(window, title, message):
    dialog = TogaModalDialog(title=title, message=message)
    dialog.add_yes_button()
    dialog.add_no_button()
    return dialog.runModal(window)


def confirm_dialog(window, title, message):
    dialog = TogaModalDialog(title=title, message=message)
    dialog.add_ok_button()
    dialog.add_cancel_button()
    return dialog.runModal(window)


def error_dialog(window, title, message):
    dialog = TogaModalDialog(title=title, message=message)
    dialog.add_ok_button()
    return dialog.runModal(window)
