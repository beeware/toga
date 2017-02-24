from rubicon.objc import *

from toga.interface import NavigationView as NavigationViewInterface

from .base import WidgetMixin
from ..libs import *


def button_for_action(callback):
    # if callback.icon == ...
    return UIBarButtonSystemItemAdd


class TogaNavigationController(UINavigationController):
    # @objc_method
    # def viewDidAppear_(self, animated: bool) -> None:
    #     print("VIEW APPEARED", animated)
    #     self.interface._update_layout()

    @objc_method
    def onAction(self):
        if self.interface.on_action:
            self.interface.on_action(self.interface)


class NavigationView(NavigationViewInterface, WidgetMixin):
    def __init__(self, title, content, on_action=None, style=None):
        super().__init__(title=title, content=content, on_action=on_action, style=style)

        self.create()

    def create(self):
        self._impl = TogaNavigationController.alloc().initWithRootViewController_(self.config[content]._impl)
        self._impl.interface = self
        self._impl.navigationBar.topItem.title = self.title

        if self.on_action:
            self._action_button = UIBarButtonItem.alloc().initWithBarButtonSystemItem_target_action_(
                button_for_action(self.on_action),
                self._impl,
                get_selector('onAction')
            )
            self._impl.navigationBar.topItem.rightBarButtonItem = self._action_button

    def _push(self, content):
        self._impl.pushViewController_animated_(content._impl, True)

    def _pop(self, content):
        self._impl.popViewController_animated_(True)
