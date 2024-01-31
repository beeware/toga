from rubicon.objc import SEL, objc_method, objc_property
from travertino.size import at_least

import toga
from toga_iOS.container import ControlledContainer
from toga_iOS.libs import UITabBarController, UITabBarItem
from toga_iOS.widgets.base import Widget


class TogaTabBarController(UITabBarController):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def tabBar_didSelectItem_(self, tabBar, item) -> None:
        # An item that actually on the tab bar has been selected
        self.performSelector(SEL("refreshContent"), withObject=None, afterDelay=0)
        # Notify of the change in selection.
        self.interface.on_select()

    @objc_method
    def navigationController_willShowViewController_animated_(
        self,
        navigationController,
        viewController,
        animated: bool,
    ) -> None:
        # An item on the "more" menu has been selected. This will also be
        # triggered for the display of the more menu itself, so we need to
        # filter for that.
        if viewController != self.moreNavigationController.viewControllers[0]:
            # If a content view is being this is an actual content view, hide
            # the back button added by the navigation view, and notify of the
            # change in selection.
            viewController.navigationItem.setHidesBackButton(True)
            self.performSelector(SEL("refreshContent"), withObject=None, afterDelay=0)
            self.interface.on_select()

    @objc_method
    def refreshContent(self) -> None:
        # Find the currently visible container, and refresh layout of the content.
        for container in self.impl.sub_containers:
            if container.controller == self.selectedViewController:
                container.content.interface.refresh()


class OptionContainer(Widget):
    uses_icons = True

    def create(self):
        self.native_controller = TogaTabBarController.alloc().init()
        self.native_controller.interface = self.interface
        self.native_controller.impl = self
        self.native_controller.delegate = self.native_controller

        # Make the tab bar non-translucent, so you can actually see it.
        self.native_controller.tabBar.setTranslucent(False)

        # The native widget representing the container is the view of the native
        # controller. This doesn't change once it's created, so we can cache it.
        self.native = self.native_controller.view

        self.sub_containers = []

        # Add the layout constraints
        self.add_constraints()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)

        # Setting the bounds changes the constraints, but that doesn't mean
        # the constraints have been fully applied. Schedule a refresh to be done
        # as soon as possible in the future
        self.native_controller.performSelector(
            SEL("refreshContent"), withObject=None, afterDelay=0
        )

    def content_refreshed(self, container):
        container.min_width = container.content.interface.layout.min_width
        container.min_height = container.content.interface.layout.min_height

    def add_option(self, index, text, widget, icon=None):
        # Create the container for the widget
        sub_container = ControlledContainer(on_refresh=self.content_refreshed)
        sub_container.content = widget
        sub_container.enabled = True
        self.sub_containers.insert(index, sub_container)

        self.configure_tab_item(sub_container, text, icon)

        self.refresh_tabs()

    def configure_tab_item(self, container, text, icon):
        # Create a UITabViewItem for the content
        container.icon = icon

        container.controller.tabBarItem = UITabBarItem.alloc().initWithTitle(
            text,
            image=(
                icon if icon else toga.Icon.OPTION_CONTAINER_DEFAULT_TAB_ICON
            )._impl.native,
            tag=0,
        )

    def remove_option(self, index):
        sub_container = self.sub_containers[index]
        sub_container.content = None
        del self.sub_containers[index]

        self.refresh_tabs()

    def refresh_tabs(self):
        self.native_controller.setViewControllers(
            [sub.controller for sub in self.sub_containers if sub.enabled],
            animated=False,
        )
        # Adding or removing a tab can cause the creation of a moreNavigationController;
        # make sure we're also the delegate for that controller.
        self.native_controller.moreNavigationController.delegate = (
            self.native_controller
        )

    def set_option_enabled(self, index, enabled):
        self.sub_containers[index].enabled = enabled
        self.refresh_tabs()

    def is_option_enabled(self, index):
        return self.sub_containers[index].enabled

    def set_option_text(self, index, text):
        self.configure_tab_item(
            self.sub_containers[index],
            text,
            self.get_option_icon(index),
        )

    def get_option_text(self, index):
        return str(self.sub_containers[index].controller.tabBarItem.title)

    def set_option_icon(self, index, icon):
        self.configure_tab_item(
            self.sub_containers[index],
            self.get_option_text(index),
            icon,
        )

    def get_option_icon(self, index):
        return self.sub_containers[index].icon

    def get_current_tab_index(self):
        # As iOS allows the user to reorder tabs, we can't use selectedIndex,
        # as that reflects the visible order, not the logical order.
        for i, container in enumerate(self.sub_containers):
            if container.controller == self.native_controller.selectedViewController:
                return i

    def set_current_tab_index(self, current_tab_index):
        # As iOS allows the user to reorder tabs, we can't use selectedIndex,
        # as that reflects the visible order, not the logical order.
        for controller in self.native_controller.viewControllers:
            if self.sub_containers[current_tab_index].controller == controller:
                self.native_controller.selectedViewController = controller
                # Setting the view controller doesn't trigger the didSelect event
                # for regular (non-"more") tabs.
                if self.native_controller.selectedIndex <= 4:
                    self.native_controller.tabBar_didSelectItem_(
                        self.native_controller.tabBar,
                        current_tab_index,
                    )

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
