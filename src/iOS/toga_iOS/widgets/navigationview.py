from rubicon.objc import *

from ..libs import *
from .base import WidgetMixin


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


class NavigationView(WidgetMixin):
    def __init__(self, title, content, on_action=None, style=None):
        super().__init__(style=style)
        self.title = title
        self.content = content
        self.on_action = on_action

        self.startup()

    def startup(self):
        self._impl = TogaNavigationController.alloc().initWithRootViewController_(self.content._impl)
        self._impl.interface = self
        self._impl.navigationBar.topItem.title = self.title

        if self.on_action:
            self._action_button = UIBarButtonItem.alloc().initWithBarButtonSystemItem_target_action_(
                button_for_action(self.on_action),
                self._impl,
                get_selector('onAction')
            )
            self._impl.navigationBar.topItem.rightBarButtonItem = self._action_button

    def _set_app(self, app):
        self.content.app = app

    def _set_window(self, window):
        self.content.window = window

    def _set_frame(self, frame):
        # print("SET FRAME", self, frame.origin.x, frame.origin.y, frame.size.width, frame.size.height)
        # self._impl.setFrame_(frame)
        # self._impl.setNeedsDisplay()
        pass
