from rubicon.objc import SEL, objc_method, objc_property
from travertino.size import at_least

from toga_iOS.container import ControlledContainer
from toga_iOS.libs import UITabBarController, UITabBarItem
from toga_iOS.widgets.base import Widget


class TogaTabBarController(UITabBarController):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def tabBar_didSelectItem_(self, tabBar, item) -> None:
        # An item that actually on the tab bar has been selected
        # Ensure that the layout of items is
        self.performSelector(SEL("refreshContent"), withObject=None, afterDelay=0)

    @objc_method
    def navigationController_willShowViewController_animated_(
        self,
        navigationController,
        viewController,
        animated: bool,
    ) -> None:
        # An item on the "more" menu has been selected.
        # This is implemented as a full NavigationController; but we don't
        # need to see the back button, as it will obscure the actual content.
        viewController.navigationItem.setHidesBackButton(True)
        self.performSelector(SEL("refreshContent"), withObject=None, afterDelay=0)

    @objc_method
    def refreshContent(self) -> None:
        # Find the currently visible container, and refresh layout of the content.
        for container in self.impl.sub_containers:
            if container.controller == self.selectedViewController:
                container.content.interface.refresh()


class OptionContainer(Widget):
    def create(self):
        print("Create tab bar controller")
        self.native_controller = TogaTabBarController.alloc().init()
        self.native_controller.interface = self.interface
        self.native_controller.impl = self
        self.native_controller.delegate = self.native_controller

        # Make the tab bar non-translucent, so you can actually see it.
        self.native_controller.tabBar.setTranslucent(False)

        print(self.native_controller.moreNavigationController)

        # The native widget representing the container is the view of the native
        # controller. This doesn't change once it's created, so we can cache it.
        self.native = self.native_controller.view

        self.sub_containers = []

        # Add the layout constraints
        self.add_constraints()

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        print("SET BOUNDS", x, y, width, height)

        # Setting the bounds changes the constraints, but that doesn't mean
        # the constraints have been fully applied. Schedule a refresh to be done
        # as soon as possible in the future
        self.native_controller.performSelector(
            SEL("refreshContent"), withObject=None, afterDelay=0
        )

    def content_refreshed(self, container):
        print("Content refreshed")
        container.min_width = container.content.interface.layout.min_width
        container.min_height = container.content.interface.layout.min_height

    def add_content(self, index, text, widget, icon=None):
        print("add content", index, text, widget)
        # Create the container for the widget
        sub_container = ControlledContainer(on_refresh=self.content_refreshed)
        sub_container.content = widget
        sub_container.enabled = True
        self.sub_containers.insert(index, sub_container)

        sub_container.controller.tabBarItem = self.create_tab_item(text, icon)

        self.refresh_tabs()

    def create_tab_item(self, text, icon):
        # Create a UITabViewItem for the content
        return UITabBarItem.alloc().initWithTitle(text, image=icon, tag=0)

    def remove_content(self, index):
        print("Remove content", index)
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
        print("Set option enabled", index, enabled)
        self.sub_containers[index].enabled = enabled
        self.refresh_tabs()

    def is_option_enabled(self, index):
        print("is option enabled", index)
        return self.sub_containers[index].enabled

    def set_option_text(self, index, value):
        print("Set option text", index, value)
        self.sub_containers[index].controller.tabBarItem = self.create_tab_item(
            value, None
        )

    def set_option_icon(self, index, value):
        print("Set option icon", index, value)
        # self.sub_containers[index].controller.tabBarItem = self.create_tab_item(value, value)

    def get_option_text(self, index):
        print("Get option text", index)
        return str(self.sub_containers[index].controller.tabBarItem.title)

    def get_current_tab_index(self):
        print("Get current tab index")
        # Although UITabBarController provides selectedIndex, it doesn't
        # handle the "more" items, and doesn't reflect hidden items.
        for i, container in enumerate(self.sub_containers):
            if container.controller == self.selectedViewController:
                return i
        return None

    def set_current_tab_index(self, current_tab_index):
        # Although UITabBarController provides selectedIndex, it (a) doesn't
        # handle the "more" items, and doesn't reflect hidden items.
        for controller in self.native.viewControllers:
            if self.sub_containers[current_tab_index].controller == controller:
                self.native.selectedViewController = controller

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
