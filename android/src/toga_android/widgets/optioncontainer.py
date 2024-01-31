from __future__ import annotations

import warnings
from dataclasses import dataclass

from android.view import MenuItem
from android.widget import LinearLayout

try:
    from com.google.android.material.bottomnavigation import BottomNavigationView
    from com.google.android.material.navigation import NavigationBarView
except ImportError:  # pragma: no cover
    # If you've got an older project that doesn't include the Material library,
    # this import will fail. We can't validate that in CI, so it's marked no cover
    BottomNavigationView = None
    NavigationBarView = None

from java import dynamic_proxy
from travertino.size import at_least

import toga

from ..container import Container
from .base import Widget


@dataclass
class TogaOption:
    text: str
    icon: toga.Icon
    widget: Widget
    enabled: bool = True
    menu_item: MenuItem | None = None


if NavigationBarView is not None:  # pragma: no branch

    class TogaOnItemSelectedListener(
        dynamic_proxy(NavigationBarView.OnItemSelectedListener)
    ):
        def __init__(self, impl):
            super().__init__()
            self.impl = impl

        def onNavigationItemSelected(self, item):
            for index, option in enumerate(self.impl.options):
                if option.menu_item == item:
                    self.impl.set_current_tab_index(index, programmatic=False)
                    return True

            # You shouldn't be able to select an item that isn't isn't selectable.
            return False  # pragma: no cover


class OptionContainer(Widget, Container):
    uses_icons = True

    def create(self):
        if BottomNavigationView is None:  # pragma: no cover
            raise RuntimeError(
                "Unable to import BottomNavigationView. Ensure that the Material "
                "system package (com.google.android.material:material:1.11.0) "
                "is listed in your app's dependencies."
            )

        self.native = LinearLayout(self._native_activity)
        self.native.setOrientation(LinearLayout.VERTICAL)

        # Define layout parameters for children; expand to fill,
        self.init_container(self.native)
        self.native_content.setLayoutParams(
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.MATCH_PARENT,
                1,  # weight 1; child content should expand
            )
        )

        # Add the navigation bar
        self.native_navigationview = BottomNavigationView(self._native_activity)
        self.native_navigationview.setLabelVisibilityMode(
            BottomNavigationView.LABEL_VISIBILITY_LABELED
        )
        self.max_items = self.native_navigationview.getMaxItemCount()

        self.native.addView(
            self.native_navigationview,
            LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT,
                0,  # weight 0; it shouldn't expand
            ),
        )

        self.onItemSelectedListener = TogaOnItemSelectedListener(self)
        self.native_navigationview.setOnItemSelectedListener(
            self.onItemSelectedListener
        )

        self.options = []

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        lp = self.native.getLayoutParams()
        super().resize_content(
            lp.width, lp.height - self.native_navigationview.getHeight()
        )

    def purge_options(self):
        for option in self.options:
            option.menu_item = None
        self.native_navigationview.getMenu().clear()

    def rebuld_options(self):
        for index, option in enumerate(self.options):
            if index < self.max_items:
                option.menu_item = self.native_navigationview.getMenu().add(
                    0, 0, index, option.text
                )
                self.set_option_icon(index, option.icon)
                self.set_option_enabled(index, option.enabled)

    def add_option(self, index, text, widget, icon=None):
        # Store the details of the new option
        option = TogaOption(text=text, icon=icon, widget=widget)
        self.options.insert(index, option)

        # Create a menu item for the tab
        if index >= self.max_items:
            warnings.warn(
                f"OptionContainer is limited to {self.max_items} items on "
                "Android. Additional item will be ignored."
            )
            option.menu_item = None
        else:
            if len(self.options) > self.max_items:
                warnings.warn(
                    f"OptionContainer is limited to {self.max_items} items on "
                    "Android. Excess items will be ignored."
                )
                last_option = self.options[self.max_items - 1]
                self.native_navigationview.getMenu().removeItem(
                    last_option.menu_item.getItemId()
                )
                last_option.menu_item = None

        # Android doesn't let you change the order index of an item after it has been
        # created, which means there's no way to insert an item into an existing
        # ordering. As a workaround, rebuild the entire navigation menu on every
        # insertion.
        self.purge_options()
        self.rebuld_options()

        # If this is the only option, make sure the content is selected
        if len(self.options) == 1:
            self.set_current_tab_index(0)

    def remove_option(self, index):
        # Android doesn't let you change the order index of an item after it has been
        # created, which means there's no way to insert an item into an existing
        # ordering. If an item is deleted, rebuild the entire navigation menu.
        self.purge_options()
        del self.options[index]
        self.rebuld_options()

    def set_option_enabled(self, index, enabled):
        option = self.options[index]
        option.enabled = enabled
        if option.menu_item:
            option.menu_item.setEnabled(enabled)

    def is_option_enabled(self, index):
        option = self.options[index]
        if option.menu_item:
            return option.menu_item.isEnabled()
        else:
            return option.enabled

    def set_option_text(self, index, text):
        option = self.options[index]
        option.text = text
        if option.menu_item:
            option.menu_item.setTitle(text)

    def get_option_text(self, index):
        option = self.options[index]
        if option.menu_item:
            return option.menu_item.getTitle()
        else:
            return option.text

    def set_option_icon(self, index, icon):
        option = self.options[index]
        option.icon = icon

        if option.menu_item:
            if icon is None:
                icon = toga.Icon.OPTION_CONTAINER_DEFAULT_TAB_ICON

            drawable = icon._impl.as_drawable(self, 32)
            option.menu_item.setIcon(drawable)

    def get_option_icon(self, index):
        return self.options[index].icon

    def get_current_tab_index(self):
        for index, option in enumerate(self.options):
            if option.menu_item.isChecked():
                return index
        # One of the tabs has to be selected
        return None  # pragma: no cover

    def set_current_tab_index(self, index, programmatic=True):
        if index < self.max_items:
            option = self.options[index]
            self.set_content(option.widget)
            option.widget.interface.refresh()
            if programmatic:
                option.menu_item.setChecked(True)
            self.interface.on_select()
        else:
            warnings.warn("Tab is outside selectable range")

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
