import platform

from rubicon.objc import SEL, objc_method, objc_property
from travertino.size import at_least

import toga
from toga_iOS.container import ControlledContainer
from toga_iOS.libs import (
    UIDevice,
    UITabBarController,
    UITabBarItem,
    UIUserInterfaceIdiom,
)
from toga_iOS.widgets.base import Widget

# Implementation note:  Delayed refresh is usually not preferred
# but is nessacary to get nested tab bars in correct place for
# some reasaon.

# FIXME:  tabbar not showing text when nested.


class TogaTabBarController(UITabBarController):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def tabBarController_didSelectViewController_(self, controller, item) -> None:
        # An item that actually on the tab bar has been selected
        self.performSelector(
            SEL("refreshContent:"), withObject=self.selectedViewController, afterDelay=0
        )
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
            #            viewController.navigationItem.setHidesBackButton(True)
            if viewController.navigationController == self.moreNavigationController:
                for container in self.impl.sub_containers:
                    if container.controller == viewController:
                        container.top_bar = True
                    else:
                        container.top_bar = False
            else:
                for container in self.impl.sub_containers:
                    container.top_bar = False
            self.performSelector(
                SEL("refreshContent:"), withObject=viewController, afterDelay=0
            )
            self.interface.on_select()

    @objc_method
    def refreshContent_(self, controller) -> None:
        # Recalculate child container offsets, as the top bar status may
        # have changed.
        if self.impl._offset_containers:
            self.impl.top_offset_children()
        else:
            self.impl.un_top_offset_children()

        # Find the currently visible container, and refresh layout of the content.
        for container in self.impl.sub_containers:
            if container.controller == controller:
                container.content.interface.refresh()


class OptionContainer(Widget):
    uses_icons = True
    unsafe_bottom = True
    un_top_offset = True

    def create(self):
        self.native_controller = TogaTabBarController.alloc().init()
        self.native_controller.interface = self.interface
        self.native_controller.impl = self
        self.native_controller.delegate = self.native_controller
        #        # FIXME:  Bug with reordering causing crash
        #        self.native_controller.customizableViewControllers = None

        if int(platform.release().split(".")[0]) < 26:  # pragma: no branch
            # Make it translucent; without this call, there will not be
            # a bottom bar at all.
            self.native_controller.tabBar.setTranslucent(True)
            self.native_controller.extendedLayoutIncludesOpaqueBars = True

        # The native widget representing the container is the view of the native
        # controller. This doesn't change once it's created, so we can cache it.
        self.native = self.native_controller.view

        self.sub_containers = []
        self._offset_containers = False

        # Add the layout constraints
        self.add_constraints()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        # Setting the bounds changes the constraints, but that doesn't mean
        # the constraints have been fully applied. Schedule a refresh to be done
        # as soon as possible in the future
        self.native_controller.performSelector(
            SEL("refreshContent:"),
            withObject=self.native_controller.selectedViewController,
            afterDelay=0,
        )

    def top_offset_children(self):
        self._offset_containers = True
        for container in self.sub_containers:
            if UIDevice.currentDevice.userInterfaceIdiom == UIUserInterfaceIdiom.Phone:
                if container.top_bar:
                    container.additional_top_offset = (
                        self.container.top_offset
                        + self.native_controller.moreNavigationController.navigationBar.frame.size.height  # noqa: E501
                    )
                else:
                    container.additional_top_offset = self.container.top_offset
            else:
                container.additional_top_offset = self.native.safeAreaInsets.top
            container.un_top_offset_able = self.container.un_top_offset_able

    def un_top_offset_children(self):
        self._offset_containers = False
        for container in self.sub_containers:
            if UIDevice.currentDevice.userInterfaceIdiom == UIUserInterfaceIdiom.Phone:
                if container.top_bar:
                    container.additional_top_offset = (
                        self.native_controller.moreNavigationController.navigationBar.frame.size.height  # noqa: E501
                    )
                else:
                    container.additional_top_offset = 0
            else:
                container.additional_top_offset = self.native.safeAreaInsets.top
            container.un_top_offset_able = False

    def content_refreshed(self, container):
        container.min_width = container.content.interface.layout.min_width
        container.min_height = container.content.interface.layout.min_height

    def add_option(self, index, text, widget, icon=None):
        # Create the container for the widget
        sub_container = ControlledContainer(
            on_refresh=self.content_refreshed, safe_bottom=True
        )
        sub_container.content = widget
        sub_container.enabled = True
        sub_container.top_bar = False
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
