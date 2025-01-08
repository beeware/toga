from android.widget import LinearLayout
from com.google.android.material.bottomnavigation import BottomNavigationView

from .base import SimpleProbe


class OptionContainerProbe(SimpleProbe):
    native_class = LinearLayout
    disabled_tab_selectable = False
    max_tabs = 5

    def __init__(self, widget):
        super().__init__(widget)
        self.native_navigationview = widget._impl.native_navigationview
        assert isinstance(self.native_navigationview, BottomNavigationView)

    def select_tab(self, index):
        item = self.native_navigationview.getMenu().getItem(index)
        # Android will let you programmatically select a disabled tab.
        if item.isEnabled():
            item.setChecked(True)
            self.impl.onItemSelectedListener(item)

    async def wait_for_tab(self, message):
        await self.redraw(message)

    def tab_enabled(self, index):
        return self.native_navigationview.getMenu().getItem(index).isEnabled()

    def assert_tab_icon(self, index, expected):
        actual = self.impl.options[index].icon
        if expected is None:
            assert actual is None
        else:
            assert actual.path.name == expected
            assert actual._impl.path.name == f"{expected}-android.png"

    def assert_tab_content(self, index, title, enabled):
        # Get the actual menu items, and sort them by their order index.
        # This *should* match the actual option order.
        menu_items = sorted(
            [option.menu_item for option in self.impl.options if option.menu_item],
            key=lambda m: m.getOrder(),
        )

        assert menu_items[index].getTitle() == title
        assert menu_items[index].isEnabled() == enabled
