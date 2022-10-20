from rubicon.objc import SEL, objc_method, objc_property

from toga.interface import NavigationView as NavigationViewInterface
from toga_iOS.libs import (
    UIBarButtonItem,
    UIBarButtonSystemItemAdd,
    UINavigationController
)
from toga_iOS.widgets.base import WidgetMixin


def button_for_action(callback):
    # if callback.icon == ...
    return UIBarButtonSystemItemAdd


class TogaNavigationController(UINavigationController):

    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

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
        self._create()

    def create(self):
        self._controller = TogaNavigationController.alloc().initWithRootViewController_(
            self._config['content']._controller
        )
        self._controller.interface = self
        self._controller.navigationBar.topItem.title = self._config['title']

        self._impl = self._controller.view

        if self._config['on_action']:
            self._action_button = UIBarButtonItem.alloc().initWithBarButtonSystemItem_target_action_(
                button_for_action(self._config['on_action']),
                self._controller,
                SEL('onAction')
            )
            self._controller.navigationBar.topItem.rightBarButtonItem = self._action_button

        # Add the layout constraints
        self._add_constraints()

    def push(self, content):
        self._controller.pushViewController_animated_(content._controller, True)

    def pop(self, content):
        self._controller.popViewController_animated_(True)
