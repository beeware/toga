from toga_iOS.libs import UITabBarController

from .base import SimpleProbe


class OptionContainerProbe(SimpleProbe):
    native_attr = "native_controller"
    native_class = UITabBarController
    disabled_tab_selectable = False
    max_tabs = None
    more_option_is_stateful = True

    @property
    def width(self):
        return self.native.frame.size.width

    @property
    def height(self):
        return self.native.frame.size.height

    def select_tab(self, index):
        # Can't select a disabled tab, so make the call a no-op.
        if self.impl.sub_containers[index].enabled:
            # selectedIndex doesn't account for disabled tabs, so
            # reduce index by the number of disabled tabs less than index
            n_disabled = sum(
                not self.impl.sub_containers[i].enabled for i in range(0, index)
            )

            self.impl.native_controller.selectedIndex = index - n_disabled
            if self.impl.native_controller.selectedIndex <= 4:
                # Programmatically selecting a tab doesn't trigger the didSelectItem event.
                self.impl.native_controller.tabBar_didSelectItem_(
                    self.impl.native_controller.tabBar,
                    index - n_disabled,
                )

    def select_more(self):
        more = self.impl.native_controller.moreNavigationController
        self.impl.native_controller.selectedViewController = more

    def reset_more(self):
        more = self.impl.native_controller.moreNavigationController
        more.popToRootViewControllerAnimated(False)

    def tab_enabled(self, index):
        return self.impl.sub_containers[index].enabled

    def assert_tab_icon(self, index, expected):
        actual = self.widget.content[index].icon
        if expected is None:
            assert actual is None
        else:
            assert actual.path.name == expected
            assert actual._impl.path.name == f"{expected}-iOS.png"
