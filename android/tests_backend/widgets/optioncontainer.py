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
        self.native_navigationview.getMenu().getItem(index).setChecked(True)

    def tab_enabled(self, index):
        return self.native_navigationview.getMenu().getItem(index).isEnabled()

    def assert_tab_icon(self, index, expected):
        actual = self.widget.content[index].icon
        if expected is None:
            assert actual is None
        else:
            assert actual.path.name == expected
            assert actual._impl.path.name == f"{expected}-android.png"
