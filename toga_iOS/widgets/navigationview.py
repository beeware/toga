from rubicon.objc import *

from ..libs import *
from .base import Widget


def button_for_action(callback):
    # if callback.icon == ...
    return UIBarButtonSystemItemAdd


class TogaNavigationController(UINavigationController):
    # @objc_method
    # def viewDidAppear_(self, animated: bool) -> None:
    #     print("VIEW APPEARED", animated)
    #     self.interface._update_layout()

    @objc_method
    def trailingAction(self):
        if self.interface.trailing_action:
            self.interface.trailing_action(self.interface)


class NavigationView(Widget):
    def __init__(self, content, trailing_action=None, **style):
        super(NavigationView, self).__init__(**style)
        self.content = content
        self.trailing_action = trailing_action

        self.startup()

    def startup(self):
        self._impl = TogaNavigationController.alloc().initWithRootViewController_(self.content._impl)
        self._impl.interface = self

        if self.trailing_action:
            self._trailing_button = UIBarButtonItem.alloc().initWithBarButtonSystemItem_target_action_(
                button_for_action(self.trailing_action),
                self._impl,
                get_selector('trailingAction')
            )
            self._impl.navigationBar.topItem.rightBarButtonItem = self._trailing_button

    def _set_app(self, app):
        self.content.app = app

    def _set_window(self, window):
        self.content.window = window

    def _set_frame(self, frame):
        # print("SET FRAME", self, frame.origin.x, frame.origin.y, frame.size.width, frame.size.height)
        # self._impl.setFrame_(frame)
        # self._impl.setNeedsDisplay()
        pass
