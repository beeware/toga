from rubicon.objc import SEL, CGRectMake, objc_method, objc_property
from travertino.size import at_least

import toga
from toga_iOS.container import ControlledContainer
from toga_iOS.libs import (
    IOS_VERSION,
    UIDevice,
    UITabBarController,
    UITabBarItem,
    UIUserInterfaceIdiom,
)
from toga_iOS.widgets.base import Widget

from ..window import navAppearance

# Implementation note:  Delayed refresh is usually not preferred
# but is nessacary to get nested tab bars in correct place for
# some reasaon.


class TogaTabBarController(UITabBarController):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def tabBarController_didSelectViewController_(self, controller, item) -> None:
        # An item that actually on the tab bar has been selected
        for container in self.impl.sub_containers:
            container.top_bar = False
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
            for container in self.impl.sub_containers:
                if container.controller == viewController:
                    container.top_bar = True
                else:
                    container.top_bar = False
            self.performSelector(
                SEL("refreshContent:"), withObject=viewController, afterDelay=0
            )
            self.interface.on_select()

    @objc_method
    def refreshContent_(self, controller) -> None:
        self.view.setNeedsLayout()
        self.view.layoutIfNeeded()
        self.customizableViewControllers = None

        # Recalculate child container offset.
        self.impl.offset_containers()

        # Find the currently visible container, and refresh layout of the content.
        for container in self.impl.sub_containers:
            if container.controller == controller:
                container.content.interface.refresh()

    @objc_method
    def updateSafeArea_(self, controller) -> None:
        is_phone = (
            UIDevice.currentDevice.userInterfaceIdiom == UIUserInterfaceIdiom.Phone
        )
        if is_phone:
            # iOS requires this hack for the "More" tab's navigation
            # bar to be placed correctly on a plain window.
            origFrame = self.view.frame
            self.view.frame = CGRectMake(
                origFrame.origin.x + 1,
                origFrame.origin.y + 1,
                origFrame.size.width,
                origFrame.size.height,
            )
            self.view.frame = origFrame
            pass
        else:
            self.view.setNeedsLayout()
        self.refreshContent(controller)


class OptionContainer(Widget):
    uses_icons = True
    unsafe_bottom = True
    un_top_offset = True

    def create(self):
        self.native_controller = TogaTabBarController.alloc().init()
        self.native_controller.interface = self.interface
        self.native_controller.impl = self
        self.native_controller.delegate = self.native_controller
        # FIXME:  Bug with reordering causing crash
        self.native_controller.customizableViewControllers = None

        if IOS_VERSION < (26, 0):  # pragma: no branch
            self.native_controller.tabBar.setTranslucent(False)
            self.native_controller.tabBar.setTranslucent(True)

        # The native widget representing the container is the view of the native
        # controller. This doesn't change once it's created, so we can cache it.
        self.native = self.native_controller.view

        self.sub_containers = []
        self._top_un_offset = False

        # Add the layout constraints
        self.add_constraints()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        # Setting bounds can cause the creation of a moreNavigationController;
        # make sure we're also the delegate for that controller.
        self.native_controller.moreNavigationController.delegate = (
            self.native_controller
        )

        if IOS_VERSION < (26, 0):  # pragma: no branch
            self.native_controller.moreNavigationController.navigationBar.standardAppearance = navAppearance  # noqa: E501

        # Setting the bounds changes the constraints, but that doesn't mean
        # the constraints have been fully applied. Schedule a refresh to be done
        # as soon as possible in the future
        self.native_controller.performSelector(
            SEL("updateSafeArea:"),
            withObject=self.native_controller.selectedViewController,
            afterDelay=0,
        )

    def top_un_offset_if_needed(self, frame):
        if (
            frame[1] == 0 and self.un_top_offset and self.container.top_offset
        ):  # pragma: no cover
            frame[1] -= self.container.top_offset
            frame[3] += self.container.top_offset
            self._top_un_offset = True
        else:
            self._top_un_offset = False
        return frame

    def offset_containers(self):  # pragma: no cover
        is_phone = (
            UIDevice.currentDevice.userInterfaceIdiom == UIUserInterfaceIdiom.Phone
        )
        top_safe_inset = (
            self.native_controller.selectedViewController.view.safeAreaInsets.top
        )

        for container in self.sub_containers:
            # If OptionContainer's top safe area is smaller than that of its view
            # controllers... that means we have a tab bar at the top on iPadOS, and
            # it's not at the bottom.
            if is_phone or (self.native.safeAreaInsets.top >= top_safe_inset):
                if self._top_un_offset:
                    container.un_top_offset_able = self.container.un_top_offset_able
                    if container.top_bar:
                        # There's no good way to monitor for the navigation bar's frame
                        # change; so we monitor it along with the safe area insets.

                        container.additional_top_offset = top_safe_inset
                        container.un_top_offset_able = top_safe_inset
                    else:
                        container.additional_top_offset = self.container.top_offset
                else:
                    container.additional_top_offset = (
                        top_safe_inset if container.top_bar else 0
                    )
                    container.un_top_offset_able = container.additional_top_offset
                container._safe_bottom = True
            else:
                # Bar is at the top here!
                container.additional_top_offset = top_safe_inset
                container.un_top_offset_able = top_safe_inset
                container._safe_bottom = False

    def content_refreshed(self, container):
        container.min_width = container.content.interface.layout.min_width
        container.min_height = container.content.interface.layout.min_height

    def content_inset_change(self):
        self.native_controller.performSelector(
            SEL("refreshContent:"),
            withObject=self.native_controller.selectedViewController,
            afterDelay=0,
        )

    def add_option(self, index, text, widget, icon=None):
        # Create the container for the widget
        # Usually we'd only want safe_bottom on iOS not iPadOS, however iPadOS windows
        # are allowed to shrink and we may end up having the tabbar go on the bottom.
        # So... we'd have to do always True.
        # TODO: Do false when we support visionOS.  Though visionOS still needs yet
        # TODO: another hack -- creating a separate controller and adding it as a child
        # TODO: Of the root.
        sub_container = ControlledContainer(
            on_refresh=self.content_refreshed,
            safe_bottom=True,
        )
        sub_container.on_inset_change = self.content_inset_change
        sub_container.content = widget
        sub_container.enabled = True
        sub_container.top_bar = False
        if IOS_VERSION < (26, 0):
            sub_container.no_webview_offset = True
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
        # FIXME:  Bug with reordering causing crash
        self.native_controller.customizableViewControllers = None

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
                    self.native_controller.tabBarController_didSelectViewController_(
                        self.native_controller,
                        self.native_controller.selectedViewController,
                    )

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
