from rubicon.objc import objc_method

from toga_iOS.libs import (
    UITabBarController,
    UITabBarItem,
    UIViewController,
)

from toga_iOS.window import iOSViewport

# from .base import Widget
from toga_iOS.widgets.base import Widget

class TogaTabBarController(UITabBarController):
    """
    Custom implememtation of the nativie IOS UITabBarController.
    Used to provide custom delegates:
        * Tab Bar Selections.
            - shouldSelect
            - didSelect
        * Tab Bar Customizations:
            - willBeginCustomizing
            - willEndCustomizing
            - didEndCustomizing
        * Rotation Settings:
            - tabBarControllerSupportedInterfaceOrientations
            - tabBarControllerPreferredInterfaceOrientationForPresentation
        * Tab Bar Transition Animations:
            - animationControllerForTransitionFrom
            - interactionControllerFor.
    """

    # @objc_method
    # def tabBarController_shouldSelectViewController_( self,
    #                                                   tbc,          # type: UITabBarController
    #                                                   vc,           # type: UIViewController
    #                                                   ) -> bool:
    #     """
    #     Event callback before tab has transitioned to new tab.
    #     """
    #
    #     # print(f'TogaTabBarController.tabBarController_shouldSelectViewController_(tbc,vc)')
    #
    #     result = True
    #     return result

    @objc_method
    def tabBarController_didSelectViewController_( self,
                                                   tbc,             # type: UITabBarController
                                                   vc,              # type: UIViewController
                                                   ) -> None:
        """
        Event callback after tab has finished transitioning to new tab.
        """

        # call the user on_select callback method (if provided)
        if self.interface.on_select:
            index = tbc.selectedIndex
            widget = tbc.interface.content[index]
            self.interface.on_select(self.interface, option=widget, index=index)

        # required to redraw new tabs correctly (possible Toga bug?)
        self.interface.refresh()

class OptionContainer(Widget):
    """
    OptionContainer implementation for the iOS platform.
    """

    def create(self):
        """
        Create native widget - iOS UITabController
        """

        self.controller = TogaTabBarController.alloc().init()
        self.controller.interface = self.interface

        self.native = self.controller.view

        self.controller.delegate = self.controller
        self.native.delegate = self.controller

        # a list of view controllers for each tab (see `add_content()`)
        self.view_controllers = []

        # self.native.translatesAutoresizingMaskIntoConstraints = False

        # Add the layout constraints
        self.add_constraints()

    def add_content(self, label, widget):
        """ Adds a new option to the option container.

        Args:
            label (str): The label for the option container
            widget: The widget or widget tree that belongs to the label.
        """

        widget.viewport = iOSViewport(widget.native)

        for child in widget.interface.children:
            child._impl.container = widget

        # tag = len(self.interface.content) - 1
        tab_bar_item = UITabBarItem.alloc().init()
        tab_bar_item.title = label

        # Turn the autoresizing mask on the widget widget
        # into constraints. This makes the widget fill the
        # available space inside the OptionContainer.
        widget.native.translatesAutoresizingMaskIntoConstraints = True

        # create view controller for the view and associate tab bar item
        vc = UIViewController.alloc().init()
        vc.view = widget.native
        vc.tabBarItem = tab_bar_item
        vc.delegate = self.controller
        widget.native.delegate = self.controller

        # append new view controller to exisiting list of view controllers
        self.view_controllers.append(vc)

        controller = self.controller
        # controller.viewControllers = self.view_controllers
        # controller.setViewControllers(self.view_controllers, animated=False)
        controller.setViewControllers(self.view_controllers, animated=True)

    def set_on_select(self, handler):
        """
        Set on_select callback handler.
        """
        pass
